from .BaseCipher import BaseCipher

import numpy as np
from numba import jit, prange


@jit(['uint8[:](uint8[:], uint8[:])'], fastmath=True)
def polydiv(u, v):
    m = len(u) - 1
    n = len(v) - 1
    q = np.zeros(max(m - n + 1, 1), dtype=np.uint8)
    r = u.copy()
    for k in range(0, m - n + 1):
        d = r[k]
        q[k] = d
        r[k:k + n + 1] = r[k:k + n + 1] - d * v
    return r


@jit(['uint8[:](uint8[:], uint8[:])'])
def polymul(a, v):
    grid = np.zeros((8, 8), dtype=np.uint8)
    for i in range(8):
        for j in range(8):
            grid[i][j] = a[i] * v[j]
    result = np.zeros(15, dtype=np.uint8)
    for k in range(15):
        if k <= 15 // 2:
            i = 0
            j = k
            for _ in range(k + 1):
                result[k] += grid[i][j]
                i = i + 1
                j = j - 1
        else:
            i = k - 7
            j = 7
            for _ in range(15 - k):
                result[k] += grid[i][j]
                i = i + 1
                j = j - 1
    return result


@jit(['uint8(uint8, uint8)'])
def galois_mult_c(b1, b2):
    p1 = np.zeros(8, dtype=np.uint8)
    p2 = np.zeros(8, dtype=np.uint8)
    c = 7
    while b1 != 0:
        p1[c] = b1 % 2
        b1 //= 2
        c -= 1
    c = 7
    while b2 != 0:
        p2[c] = b2 % 2
        b2 //= 2
        c -= 1
    g_mult = polymul(p1, p2)
    const_divisor = np.array([1, 0, 0, 0, 1, 1, 0, 1, 1], dtype=np.uint8)
    res = polydiv(g_mult, const_divisor)
    result = 0
    c = res.shape[0] - 1
    for i in prange(c + 1):
        result = result | ((res[i] % 2) << c)
        c -= 1
    return result


@jit(['uint8[:](uint8[:], int8)'])
def roll(array, p):
    result_array = np.empty_like(array)
    size = array.shape[0]
    if p > size:
        p = p % size
    if p < 0:
        p = -p
        left_part = array[:p].copy()
        right_part = array[p:].copy()
        result_array[: size - p] = right_part
        result_array[size - p:] = left_part
    elif p > 0:
        left_part = array[:size - p].copy()
        right_part = array[size - p:].copy()
        result_array[: p] = right_part
        result_array[p:] = left_part
    return result_array


@jit(['uint8[:, :](uint8[:, :])'])
def MixColumns_c(state):
    for i in range(4):
        col = state[:, i].copy()
        state[0][i] = galois_mult_c(0x2, col[0]) ^ galois_mult_c(0x3, col[1]) ^ col[2] ^ col[3]
        state[1][i] = col[0] ^ galois_mult_c(0x2, col[1]) ^ galois_mult_c(0x3, col[2]) ^ col[3]
        state[2][i] = col[0] ^ col[1] ^ galois_mult_c(0x2, col[2]) ^ galois_mult_c(0x3, col[3])
        state[3][i] = galois_mult_c(0x3, col[0]) ^ col[1] ^ col[2] ^ galois_mult_c(0x2, col[3])
    return state


@jit(['uint8[:](uint8[:])'])
def bin_to_hex(bin_array):
    hex_array = np.zeros(bin_array.size // 8, dtype=np.uint8)
    for i in range(bin_array.size // 8):
        bin_slice = bin_array[8 * i: 8 * i + 8]
        p = 7
        for j in range(8):
            hex_array[i] += bin_slice[j] * 2 ** p
            p -= 1
    return hex_array


class AES(BaseCipher):
    Sbox = np.array([[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                     [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                     [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                     [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                     [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                     [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                     [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                     [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                     [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                     [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                     [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                     [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                     [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                     [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                     [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                     [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]],
                    dtype=np.uint8)

    Rcon = np.array([[0x00, 0x00, 0x00, 0x00],
                     [0x01, 0x00, 0x00, 0x00],
                     [0x02, 0x00, 0x00, 0x00],
                     [0x04, 0x00, 0x00, 0x00],
                     [0x08, 0x00, 0x00, 0x00],
                     [0x10, 0x00, 0x00, 0x00],
                     [0x20, 0x00, 0x00, 0x00],
                     [0x40, 0x00, 0x00, 0x00],
                     [0x80, 0x00, 0x00, 0x00],
                     [0x1b, 0x00, 0x00, 0x00],
                     [0x36, 0x00, 0x00, 0x00]], dtype=np.uint8)

    def __init__(self, mode, n_rounds=None):
        if mode == 128:
            self.Nr = 10
            self.Nk = 4
        elif mode == 192:
            self.Nr = 12
            self.Nk = 6
        elif mode == 256:
            self.Nr = 14
            self.Nk = 8
        self.Nb = 4
        self.plain_text = None
        self.cipher_key = None
        self.iv = None

        self.round_keys = None
        self.cipher_text = None
        self.encr_blocks = None

        if n_rounds is None:
            self.encrypt = self.encrypt_one_block
        elif isinstance(n_rounds, int) and n_rounds > 1:
            self.encrypt = self.custom_round_encryption
        else:
            raise AttributeError('Wrong number of rounds')
        self.n_rounds = n_rounds

        self.bytes_per_block = 16

        super().__init__(self.bytes_per_block)

    def _set_cipherkey(self, key):
        self.cipher_key = key
        self.KeyExpansion()

    def _set_plaintext(self, PT):
        self.plain_text = PT
        return 0

    def set_plaintext_hex(self, hex_array):
        self._set_plaintext(hex_array)

    def set_plaintext_bin(self, bin_array):
        hex_array = bin_to_hex(bin_array)
        self._set_plaintext(hex_array)

    def set_key_hex(self, hex_array):
        self._set_cipherkey(hex_array)

    def set_key_bin(self, bin_array):
        hex_array = bin_to_hex(bin_array)
        self._set_cipherkey(hex_array)

    def set_iv_hex(self, hex_array):
        self.iv = hex_array

    def set_iv_bin(self, bin_array):
        self.iv = bin_to_hex(bin_array)

    def get_ciphertext(self):
        return self.cipher_text

    def SubBytes(self, state):
        new_state = np.zeros_like(state)
        for i in range(state.shape[0]):
            for j in range(self.Nb):
                n = state[i][j]
                x = n >> 4
                y = n & 0xf
                new_state[i][j] = self.Sbox[x][y]
        return new_state

    def SubWord(self, word):
        new_word = np.zeros_like(word, dtype=np.uint8)
        for i in range(word.shape[0]):
            n = word[i]
            x = n >> 4
            y = n & 0xf
            new_word[i] = AES.Sbox[x][y]
        return new_word

    def ShiftRows(self, state):
        for row in range(1, 4):
            state[row] = roll(state[row].astype(np.uint8), -row)
        return state

    @staticmethod
    def galois_mult(b1, b2):
        result = galois_mult_c(b1, b2)
        return result

    def MixColumns(self, state):
        return MixColumns_c(state)

    def AddRoundKey(self, state, RK):
        return state ^ RK

    def KeyExpansion(self):
        w = np.zeros((self.Nb * (self.Nr + 1), 4), dtype=np.uint8)
        i = 0
        while i < self.Nk:
            w[i] = np.array([self.cipher_key[4 * i], self.cipher_key[4 * i + 1], self.cipher_key[4 * i + 2],
                             self.cipher_key[4 * i + 3]])
            i += 1
        i = self.Nk
        while i < self.Nb * (self.Nr + 1):
            temp = w[i - 1].copy()
            if i % self.Nk == 0:
                after_rotword = roll(temp, -1)
                after_subword = self.SubWord(after_rotword)
                temp = after_subword ^ AES.Rcon[int(i / self.Nk)]
            elif self.Nk > 6 and i % self.Nk == 4:
                temp = self.SubWord(temp)
            w[i] = w[i - self.Nk] ^ temp
            i += 1
        F_W = np.zeros((self.Nr + 1, 4, self.Nb), dtype=np.object)
        c = 0
        for i in range(self.Nr + 1):
            for j in range(4):
                for k in range(self.Nb):
                    F_W[i][j][k] = w[c][k]
                c += 1
        self.round_keys = F_W.astype(np.uint8)
        return F_W.astype(np.uint8)

    def InToState(self, IN):
        state = np.zeros((4, self.Nb), dtype=np.uint8)
        for r in range(4):
            for c in range(self.Nb):
                state[r][c] = IN[r + 4 * c]
        return state

    def StateToOut(self, state):
        out = np.zeros(4 * self.Nb, dtype=np.uint8)
        for r in range(4):
            for c in range(self.Nb):
                out[r + 4 * c] = state[r][c]
        return out

    @staticmethod
    def StateToHex(state):
        hexstate = np.zeros_like(state, dtype='<U4')
        for r in range(state.shape[0]):
            for c in range(state.shape[1]):
                hexstate[r][c] = hex(state[r][c])
        return hexstate

    def encrypt_one_block(self, plain_block):
        one_block = plain_block.copy()
        state = self.InToState(one_block)
        state = self.AddRoundKey(state, self.round_keys[0].T)
        for R in range(1, self.Nr):
            state = self.SubBytes(state)
            state = self.ShiftRows(state)
            state = self.MixColumns(state)
            state = self.AddRoundKey(state, self.round_keys[R].T)
        state = self.SubBytes(state)
        state = self.ShiftRows(state)
        state = self.AddRoundKey(state, self.round_keys[self.Nr].T)
        out = self.StateToOut(state)
        return out

    def _one_round_encryption(self, state_old, round_key=None):
        if round_key is None:
            round_key = np.random.randint(low=0, high=256, size=(4, 4), dtype=np.uint8)
        state = self.SubBytes(state_old)
        state = self.ShiftRows(state)
        state = self.MixColumns(state)
        state = self.AddRoundKey(state, round_key)
        return state

    def custom_round_encryption(self, plain_block):
        one_block = plain_block.copy()
        state = self.InToState(one_block)
        state ^= np.random.randint(low=0, high=256, size=(4, 4), dtype=np.uint8)
        for R in range(1, self.n_rounds):
            state = self._one_round_encryption(state_old=state)
        state = self.SubBytes(state)
        state = self.ShiftRows(state)
        state = self.AddRoundKey(state, np.random.randint(low=0, high=256, size=(4, 4), dtype=np.uint8))
        out = self.StateToOut(state)
        return out

### AES-128 ###

# ciper_AES128 = AES_cipher(4, 10, 4)
# plaintext = np.array([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
# key = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])
# ciper_AES128.set_plaintext(plaintext)
# ciper_AES128.set_cipherkey(key)
# ciper_AES128.encrypt()
# ciper_AES128.get_ciphertext()
#
#
## AES-192 ###
# cipher_AES192 = AES_cipher(4, 12, 6)
# plaintext = np.array([0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xaa,0xbb,0xcc,0xdd,0xee,0xff])
# key = np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x10,
#                 0x11,0x12,0x13,0x14,0x15,0x16,0x17])
# ciper_AES128.set_plaintext(plaintext)
# ciper_AES128.set_cipherkey(key)
# ciper_AES128.encrypt()
# ciper_AES128.get_ciphertext()

### AES-256 ###
# cipher_AES256 = AES_cipher(256)
# plaintext = np.array([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
# key = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10,
#                 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f])
# plaintext = np.random.randint(low=0, high=255, size=16*1024)
# cipher_AES256.set_plaintext(plaintext)
# cipher_AES256.set_cipherkey(key)
# start_time = time.time()
# cipher_AES256.ECB_mode()
# stop_time = time.time() - start_time
# print('Encryption: ', stop_time, 's')
# print(cipher_AES256.BitOutput())

### TEST CBC MODE ###
# plaintext = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
#                       0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f])
# cipherkey = np.array([0xc2, 0x86, 0x69, 0x6d, 0x88, 0x7c, 0x9a, 0xa0, 0x61, 0x1b, 0xbb, 0x3e, 0x20, 0x25, 0xa4, 0x5a])
# cbc_iv = np.array([0x56, 0x2e, 0x17, 0x99, 0x6d, 0x09, 0x3d, 0x28, 0xdd, 0xb3, 0xba, 0x69, 0x5a, 0x2e, 0x6f, 0x58])
# cbc_exp = np.array([0xd2, 0x96, 0xcd, 0x94, 0xc2, 0xcc, 0xcf, 0x8a, 0x3a, 0x86, 0x30, 0x28, 0xb5, 0xe1, 0xdc, 0x0a,
#                     0x75, 0x86, 0x60, 0x2d, 0x25, 0x3c, 0xff, 0xf9, 0x1b, 0x82, 0x66, 0xbe, 0xa6, 0xd6, 0x1a, 0xb1])
#
# cipher = AES_cipher(128)
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipherkey)
# cipher.CBC_mode(cbc_iv)
# print(f"CBC exp: {cbc_exp}")
# print(f"CBC obs: {bit_to_hex_array(cipher.BitOutput())}")

# def hex2bin(hex_array):
#     bin_array = np.zeros(hex_array.size * 8, dtype=np.uint8)
#     for i in range(hex_array.size):
#         hex_num = hex_array[i]
#         bin_slice = bin_array[8 * i:8 * i + 8]
#         p = 7
#         while hex_num > 0:
#             bin_slice[p] = hex_num % 2
#             hex_num //= 2
#             p -= 1
#     return bin_array
#
#
# ### TEST ECB MODE ###
# plaintext_hex = np.array(
#     [0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
# plaintext_bin = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,
#                        1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
#                        0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0,
#                        0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0,
#                        1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1,
#                        0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.uint8)
# # test_pt = np.array([0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34])
# # test_ck2 = np.array([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
# cipherkey_hex = np.array(
#     [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])
# cipherkey_bin = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
#                        1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
#                        0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,
#                        0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0,
#                        0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1,
#                        0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1], dtype=np.uint8)
# # test_ck = np.array([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
# ecb_out_hex = np.array([0x69, 0xc4, 0xe0, 0xd8, 0x6a, 0x7b, 0x04, 0x30, 0xd8, 0xcd, 0xb7, 0x80, 0x70, 0xb4, 0xc5, 0x5a])
# ecb_out_bin = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0,
#                      0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1,
#                      1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
#                      0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1,
#                      1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1,
#                      0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0], dtype=np.uint8)
# #
# print('FULL HEX input')
# cipher_hex = AES(128)
# cipher_hex.set_plaintext_hex(plaintext_hex)
# cipher_hex.set_key_hex(cipherkey_hex)
# cipher_hex.ECB_mode()
# encr_hex = bit_to_hex_array(cipher_hex.BitOutput())
# print('Expected Output HEX:', ecb_out_hex)
# print('Encrypted Output HEX:', encr_hex)
# print('SUM (XOR):', (ecb_out_hex^encr_hex).sum())
#
# # print(ecb_out_hex)
# # hex_output = bit_to_hex_array(cipher_hex.BitOutput())
# # print(bit_to_hex_array(cipher_hex.BitOutput()))
# # print('SUM ', (hex_output ^ bit_to_hex_array((cipher_hex.BitOutput()))).sum())
#
#
# print('FULL BIN input')
# cipher_bin = AES(128)
# cipher_bin.set_plaintext_bin(plaintext_bin)
# cipher_bin.set_key_bin(cipherkey_bin)
# cipher_bin.ECB_mode()
# encr_bin = cipher_bin.BitOutput()
# print('Expected Output BIN:', ecb_out_bin)
# print('Encrypted Output BIN:', encr_bin)
# print('SUM (XOR):', (ecb_out_bin^encr_bin).sum())

# print(ecb_out_bin)
# bin_output = cipher_bin.BitOutput()
# print(cipher_bin.BitOutput())
# print('SUM: ', (bin_output ^ cipher_bin.BitOutput()).sum())
