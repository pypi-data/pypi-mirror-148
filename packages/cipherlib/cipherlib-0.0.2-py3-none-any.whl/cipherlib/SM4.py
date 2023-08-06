import numpy as np
from tqdm import tqdm


class SM4_cipher:
    Sbox = np.array([[0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05],
                     [0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99],
                     [0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62],
                     [0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6],
                     [0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8],
                     [0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35],
                     [0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87],
                     [0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e],
                     [0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1],
                     [0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3],
                     [0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f],
                     [0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51],
                     [0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8],
                     [0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0],
                     [0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84],
                     [0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]])

    FK = np.array([0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc])

    CK = np.array([0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
                   0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
                   0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
                   0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
                   0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
                   0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
                   0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
                   0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279])

    def __init__(self):
        self.round_keys = None
        self.plain_text = None
        self.cipher_key = None
        self.encr_blocks = None

    def set_plaintext(self, plaintext):
        self.plain_text = plaintext

    def set_cipherkey(self, cipherkey):
        self.cipher_key = cipherkey
        self.KeyExpansion()

    def BitOutput(self):
        byte_arr = self.encr_blocks.copy()
        bit_arr = np.zeros(128 * byte_arr.shape[0], dtype=np.int8)
        for j in range(byte_arr.shape[0]):
            for i in range(byte_arr.shape[1]):
                one_byte = byte_arr[j][i]
                bit8 = bit_arr[128 * j + 8 * i: 128 * j + 8 * i + 8]
                p = 7
                while one_byte != 0:
                    bit8[p] = one_byte % 2
                    one_byte //= 2
                    p -= 1
        return bit_arr

    def hexArrayToWord(self, arr):
        word = 0
        s = 24
        for i in range(arr.shape[0]):
            word = word | (arr[i] << s)
            s -= 8
        assert word <= 2 ** 32
        return word

    def binArrayToWord(self, arr):
        n = 0
        p = 31
        for i in range(arr.shape[0]):
            n += arr[i] * (2 ** p)
            p -= 1
        assert n <= 2 ** 32
        return n

    def L(self, W):
        s_word = np.zeros(32, dtype=np.int8)
        p = 31
        while W != 0:
            s_word[p] = W % 2
            W //= 2
            p -= 1
        return s_word ^ np.roll(s_word, -2) ^ np.roll(s_word, -10) ^ np.roll(s_word, -18) ^ np.roll(s_word, -24)

    def T(self, W):
        new_word = np.zeros(4, dtype=int)
        for i in range(4):
            byte = W & 0xff
            x = byte >> 4
            y = byte & 0xf
            new_word[i] = self.Sbox[x][y]
            W = W >> 8
        return self.binArrayToWord(self.L(self.hexArrayToWord(new_word)))

    def F(self, X0, X1, X2, X3, rk):
        return X0 ^ self.T(X1 ^ X2 ^ X3 ^ rk)

    def BytesToOutput(self, X):
        out = ''
        for i in range(4):
            out += format(X[i], 'x')
        return out

    def L_key(self, W):
        s_word = np.zeros(32, dtype=np.int8)
        p = 31
        while W != 0:
            s_word[p] = W % 2
            W //= 2
            p -= 1
        return s_word ^ np.roll(s_word, -13) ^ np.roll(s_word, -23)

    def T_key(self, W):
        new_word = np.zeros(4, dtype=int)
        for i in range(4):
            byte = W & 0xff
            x = byte >> 4
            y = byte & 0xf
            new_word[i] = self.Sbox[x][y]
            W = W >> 8
        return self.binArrayToWord(self.L_key(self.hexArrayToWord(new_word)))

    def KeyExpansion(self):
        K = np.zeros(36, dtype=np.object)
        K[0], K[1], K[2], K[3] = np.array_split(self.cipher_key, 4)
        K[0] = self.hexArrayToWord(K[0]) ^ self.FK[0]
        K[1] = self.hexArrayToWord(K[1]) ^ self.FK[1]
        K[2] = self.hexArrayToWord(K[2]) ^ self.FK[2]
        K[3] = self.hexArrayToWord(K[3]) ^ self.FK[3]
        for i in range(4, 36):
            K[i] = K[i - 4] ^ self.T_key(K[i - 3] ^ K[i - 2] ^ K[i - 1] ^ self.CK[i - 4])
        self.round_keys = K
        return 0

    def WordArrayToHex(self, word_arr):
        byte_arr = np.zeros(word_arr.shape[0] * 4, dtype=np.int64)
        for i in range(word_arr.shape[0]):
            word = word_arr[i]
            byte_arr[4 * i] = word >> 24
            byte_arr[4 * i + 1] = (word >> 16) & 0xff
            byte_arr[4 * i + 2] = (word >> 8) & 0xff
            byte_arr[4 * i + 3] = word & 0xff
        return byte_arr

    def encrypt_one_block(self, plain_block):
        one_block = plain_block.copy()
        X = np.zeros(36, dtype=np.object)
        X[0], X[1], X[2], X[3] = np.array_split(one_block, 4)
        X[0] = self.hexArrayToWord(X[0])
        X[1] = self.hexArrayToWord(X[1])
        X[2] = self.hexArrayToWord(X[2])
        X[3] = self.hexArrayToWord(X[3])
        for i in range(4, 36):
            X[i] = self.F(X[i - 4], X[i - 3], X[i - 2], X[i - 1], self.round_keys[i])
        word_arr = np.array(([X[35], X[34], X[33], X[32]]))
        return self.WordArrayToHex(word_arr)

    def one_round_encryption(self, plain_block, X4=np.array([]), round_key=None):
        if round_key is None:
            round_key = np.random.randint(0, 2 ** 32 - 1, size=1)[0]
        if X4.size == 0:
            X4 = np.random.randint(0, 2 ** 32 - 1, size=4)
        X_out = self.F(X4[0], X4[1], X4[2], X4[3], round_key)
        return X_out

    def ArrayToBlocks(self, init_vec=np.array([])):
        size = self.plain_text.shape[0]
        if 0 < size / 16 - int(size / 16) <= 0.5:
            n_blocks = int(size / 16 + 1)
        elif 0.5 < size / 16 - int(size / 16) < 1:
            n_blocks = int(size / 16) + 1
        else:
            n_blocks = size // 16
        if init_vec.size != 0:
            blocks = np.zeros((n_blocks + 1, 16), dtype=np.int64)
            blocks[0] = init_vec
            for i in range(1, n_blocks):
                if i != n_blocks - 1:
                    for j in range(16):
                        blocks[i][j] = self.plain_text[16 * i + j]
                else:
                    p = 0
                    for j in range(16 * (n_blocks - 1), size):
                        blocks[i][p] = self.plain_text[j]
                        p += 1
        else:
            blocks = np.zeros((n_blocks, 16), dtype=np.int64)
            for i in range(n_blocks):
                if i != n_blocks - 1:
                    for j in range(16):
                        blocks[i][j] = self.plain_text[16 * i + j]
                else:
                    p = 0
                    for j in range(16 * (n_blocks - 1), size):
                        blocks[i][p] = self.plain_text[j]
                        p += 1
        return blocks

    def ECB_mode(self):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros_like(plain_blocks)
        for i in tqdm(range(n_blocks)):
            encr_blocks[i] = self.encrypt_one_block(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks

    def CBC_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros((n_blocks + 1, 16), dtype=np.int64)
        encr_blocks[0] = init_vec
        for i in tqdm(range(n_blocks)):
            plain_blocks[i] = plain_blocks[i] ^ encr_blocks[i]
            encr_blocks[i + 1] = self.encrypt_one_block(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks[1:]

    def CFB_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks(init_vec)
        n_blocks = plain_blocks.shape[0] - 1
        encr_blocks = np.zeros((n_blocks, 16), dtype=np.int64)
        first_block = self.encrypt_one_block(plain_blocks[0]) ^ plain_blocks[1]
        encr_blocks[0] = first_block
        for i in tqdm(range(1, n_blocks)):
            encr_blocks[i] = self.encrypt_one_block(encr_blocks[i - 1]) ^ plain_blocks[i + 1]
        self.encr_blocks = encr_blocks
        return encr_blocks

    def OFB_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros_like(plain_blocks)
        temp = np.zeros_like(plain_blocks)
        temp[0] = self.encrypt_one_block(init_vec)
        encr_blocks[0] = temp[0] ^ plain_blocks[0]
        for i in tqdm(range(1, n_blocks)):
            temp[i] = self.encrypt_one_block(temp[i - 1])
            encr_blocks[i] = temp[i] ^ plain_blocks[i]
        self.encr_blocks = encr_blocks
        return encr_blocks


# plaintext = np.random.randint(low=0, high=255, size=128)
# plaintext = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10])
# cipher_key = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef, 0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10])
#
# cipher = SM4_cipher()
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipher_key)
# cipher.ECB_mode()
# print(cipher.BinOutput())
# print(cipher.one_round_encryption(np.random.randint(0, 255, size=16)))

def bit_to_hex_array(bit_array: np.ndarray):
    hex_array = np.zeros(bit_array.size // 8)
    for i in range(hex_array.size):
        bit_slice = bit_array[8*i: 8*i+8]
        p = 7
        for j in range(bit_slice.size):
            hex_array[i] += bit_slice[j] * 2 ** p
            p -= 1
    return hex_array


# plaintext = np.array([0xAA, 0xAA, 0xAA, 0xAA, 0xBB, 0xBB, 0xBB, 0xBB, 0xCC, 0xCC, 0xCC, 0xCC, 0xDD, 0xDD, 0xDD, 0xDD,
#                       0xEE, 0xEE, 0xEE, 0xEE, 0xFF, 0xFF, 0xFF, 0xFF, 0xAA, 0xAA, 0xAA, 0xAA, 0xBB, 0xBB, 0xBB, 0xBB])
# cipherkey = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
# cbc_iv = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
# cbc_result = np.array([0x78, 0xEB, 0xB1, 0x1C, 0xC4, 0x0B, 0x0A, 0x48, 0x31, 0x2A, 0xAE, 0xB2, 0x04, 0x02, 0x44, 0xCB,
#                        0x4C, 0xB7, 0x01, 0x69, 0x51, 0x90, 0x92, 0x26, 0x97, 0x9B, 0x0D, 0x15, 0xDC, 0x6A, 0x8F, 0x6D])
# ecb_result = np.array([0x5E, 0xC8, 0x14, 0x3D, 0xE5, 0x09, 0xCF, 0xF7, 0xB5, 0x17, 0x9F, 0x8F, 0x47, 0x4B, 0x86, 0x19,
#                        0x2F, 0x1D, 0x30, 0x5A, 0x7F, 0xB1, 0x7D, 0xF9, 0x85, 0xF8, 0x1C, 0x84, 0x82, 0x19, 0x23, 0x04])
#
# cipher = SM4_cipher()
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipherkey)
# cipher.CBC_mode(cbc_iv)
# cipher.ECB_mode()
# print('CBC expected', ecb_result)
# print('CBC observed', bit_to_hex_array(cipher.BitOutput()))

# plaintext = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
# cipherkey = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
# ecb_exp = np.array([0x68, 0x1E, 0xDF, 0x34, 0xD2, 0x06, 0x96, 0x5E, 0x86, 0xB3, 0xE9, 0x4F, 0x53, 0x6E, 0x42, 0x46])
# cipher = SM4_cipher()
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipherkey)
# cipher.ECB_mode()
# print(f'ECB exp: {ecb_exp}')
# print(f'ECB obs: {bit_to_hex_array(cipher.BitOutput())}')
#

def bit_to_hex_array(bit_array: np.ndarray):
    hex_array = np.zeros(bit_array.size // 8)
    for i in range(hex_array.size):
        bit_slice = bit_array[8*i: 8*i+8]
        p = 7
        for j in range(bit_slice.size):
            hex_array[i] += bit_slice[j] * 2 ** p
            p -= 1
    return hex_array


# plaintext = np.array([0xAA, 0xAA, 0xAA, 0xAA, 0xBB, 0xBB, 0xBB, 0xBB, 0xCC, 0xCC, 0xCC, 0xCC, 0xDD, 0xDD, 0xDD, 0xDD,
#                       0xEE, 0xEE, 0xEE, 0xEE, 0xFF, 0xFF, 0xFF, 0xFF, 0xAA, 0xAA, 0xAA, 0xAA, 0xBB, 0xBB, 0xBB, 0xBB])
# cipherkey = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
# cbc_iv = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F])
# cbc_result = np.array([0x78, 0xEB, 0xB1, 0x1C, 0xC4, 0x0B, 0x0A, 0x48, 0x31, 0x2A, 0xAE, 0xB2, 0x04, 0x02, 0x44, 0xCB,
#                        0x4C, 0xB7, 0x01, 0x69, 0x51, 0x90, 0x92, 0x26, 0x97, 0x9B, 0x0D, 0x15, 0xDC, 0x6A, 0x8F, 0x6D])
# ecb_result = np.array([0x5E, 0xC8, 0x14, 0x3D, 0xE5, 0x09, 0xCF, 0xF7, 0xB5, 0x17, 0x9F, 0x8F, 0x47, 0x4B, 0x86, 0x19,
#                        0x2F, 0x1D, 0x30, 0x5A, 0x7F, 0xB1, 0x7D, 0xF9, 0x85, 0xF8, 0x1C, 0x84, 0x82, 0x19, 0x23, 0x04])
#
# cipher = SM4_cipher()
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipherkey)
# cipher.CBC_mode(cbc_iv)
# cipher.ECB_mode()
# print('CBC expected', ecb_result)
# print('CBC observed', bit_to_hex_array(cipher.BitOutput()))

# plaintext = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
# cipherkey = np.array([0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10])
# ecb_exp = np.array([0x68, 0x1E, 0xDF, 0x34, 0xD2, 0x06, 0x96, 0x5E, 0x86, 0xB3, 0xE9, 0x4F, 0x53, 0x6E, 0x42, 0x46])
# cipher = SM4_cipher()
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipherkey)
# cipher.ECB_mode()
# print(f'ECB exp: {ecb_exp}')
# print(f'ECB obs: {bit_to_hex_array(cipher.BitOutput())}')
#
