import numpy as np
import scipy.stats as sts
from tqdm import tqdm
from numba import jit


@jit(['int8[:](int8[:], int64[:, :], int64[:, :, :])'], fastmath=True)
def encrypt_one_block_c(plain_text, round_keys, S):
    # FIXME проверить типы
    IP = np.array([57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61,
                   53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48,
                   40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44,
                   36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6])
    E = np.array([31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11,
                  12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22,
                  23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0])
    P = np.array([15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1,
                  7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24])
    IP_inv = np.array([39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37,
                       5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3,
                       43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,
                       9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24])
    plaintext = plain_text.copy()
    round_keys = round_keys.copy()
    M = plaintext[IP]
    Kn = round_keys
    LnRn = np.zeros((17, 2, 32), dtype=np.int8)
    # LnRn[0] = np.array_split(M, 2)
    LnRn[0][0] = M[0: M.shape[0] // 2]
    LnRn[0][1] = M[M.shape[0] // 2:]
    for i in range(1, 17):
        Output = np.zeros(32, dtype=np.int8)
        counter = 0
        LnRn[i][0] = LnRn[i - 1][1]
        B = np.zeros((8, 6), dtype=np.int8)
        _b_i = Kn[i - 1] ^ LnRn[i - 1][1][E]
        for b_i in range(8):
            B[b_i] = _b_i[6 * b_i: 6 * b_i + 6]
        for k in range(8):
            B_k = B[k]
            I = (B_k[0] << 1) | B_k[-1]
            J = (B_k[1] << 3) | (B_k[2] << 2) | (B_k[3] << 1) | B_k[4]
            S_o = S[k][I][J]
            for c in range(4):
                Output[counter] = (S_o >> (3 - c)) & 0x1
                counter += 1
        f = Output[P]
        LnRn[i][1] = LnRn[i - 1][0] ^ f
    RL16 = np.concatenate((LnRn[16][1], LnRn[16][0]))
    final_code = RL16[IP_inv]
    return final_code


class DES_cipher:
    def __init__(self):
        self.plain_text = None
        self.cipher_key = None
        self.encr_blocks = None
        self.PC_1 = np.array([56, 48, 40, 32, 24, 16, 8, 0, 57, 49, 41, 33, 25, 17, 9, 1, 58,
                              50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 62, 54, 46, 38, 30, 22,
                              14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 60, 52, 44, 36, 28, 20, 12,
                              4, 27, 19, 11, 3])
        self.shifts_list = np.array([1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1])
        self.PC_2 = np.array([13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25,
                              7, 15, 6, 26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39, 50, 44,
                              32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31])
        self.IP = np.array([57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61,
                            53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48,
                            40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44,
                            36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6])
        self.E = np.array([31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11,
                           12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22,
                           23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0])
        self.S1 = np.array([[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]])
        self.S2 = np.array([[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]])
        self.S3 = np.array([[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]])
        self.S4 = np.array([[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]])
        self.S5 = np.array([[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]])
        self.S6 = np.array([[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]])
        self.S7 = np.array([[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]])
        self.S8 = np.array([[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]])
        self.S = np.array([self.S1, self.S2, self.S3, self.S4, self.S5, self.S6, self.S7, self.S8])
        self.P = np.array([15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1,
                           7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24])
        self.IP_inv = np.array([39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37,
                                5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3,
                                43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41,
                                9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24])

    def BitOutput(self):
        out = np.zeros(64 * self.encr_blocks.shape[0], dtype=np.int8)
        for i in tqdm(range(self.encr_blocks.shape[0]), desc='Saving'):
            out[64 * i: 64 * i + 64] = self.encr_blocks[i]
        return out

    def set_cipherkey(self, key):
        self.cipher_key = key

    def set_plaintext(self, PT):
        self.plain_text = PT

    def get_ciphertext(self):
        return self.cipher_text

    def cycle_shift(self, array, steps, direction=1):
        """
        direction = 1: right shift
        direction = -1: left shift
        """
        return np.roll(array, steps * direction)

    def KeyExpansion(self, cipher_key):
        K_plus = cipher_key[self.PC_1]
        Cn_Dn = np.zeros((17, 2), dtype=np.object)
        Cn_Dn[0][0], Cn_Dn[0][1] = np.array_split(K_plus, 2)
        for i in range(1, 17):
            Cn_Dn[i][0] = self.cycle_shift(Cn_Dn[i - 1][0], self.shifts_list[i - 1], -1)
            Cn_Dn[i][1] = self.cycle_shift(Cn_Dn[i - 1][1], self.shifts_list[i - 1], -1)
        Kn = np.zeros((16, 48), dtype=np.int64)
        for i in range(16):
            CD_i = np.concatenate((Cn_Dn[i + 1][0], Cn_Dn[i + 1][1]))
            Kn[i] = CD_i[self.PC_2]
        return Kn

    def encrypt_one_block(self, plain_text):
        round_keys = self.KeyExpansion(self.cipher_key)
        final_code = encrypt_one_block_c(plain_text, round_keys, self.S)
        return final_code

    def one_round_encryption(self, left_part_old, right_part_old, round_key=np.array([])):
        if round_key.size == 0:
            round_key = sts.bernoulli.rvs(0.5, size=right_part_old.shape[0])
        out_block = np.zeros(32, dtype=np.int8)
        c = 3
        left_part = right_part_old
        B = np.array_split(round_key ^ right_part_old[self.E], 8)
        for k in range(8):
            B_k = B[k]
            x = (B_k[0] << 1) | B_k[5]
            y = (B_k[1] << 3) | (B_k[2] << 2) | (B_k[3] << 1) | B_k[4]
            sbox_out = self.S[k][x][y]
            while sbox_out != 0:
                out_block[c] = sbox_out % 2
                sbox_out //= 2
                c -= 1
            c = 3
        right_part = left_part_old ^ out_block[self.P]
        return left_part, right_part

    def ArrayToBlocks(self, init_vec=np.array([])):
        size = self.plain_text.shape[0]
        if 0 < size / 64 - int(size / 64) <= 0.5:
            n_blocks = int(size / 64 + 1)
        elif 0.5 < size / 64 - int(size / 64) < 1:
            n_blocks = int(size / 64) + 1
        else:
            n_blocks = size // 64
        if init_vec.size != 0:
            blocks = np.zeros((n_blocks + 1, 64), dtype=np.int8)
            blocks[0] = init_vec
            for i in range(1, n_blocks):
                if i != n_blocks - 1:
                    for j in range(64):
                        blocks[i][j] = self.plain_text[64 * i + j]
                else:
                    p = 0
                    for j in range(64 * (n_blocks - 1), size):
                        blocks[i][p] = self.plain_text[j]
                        p += 1
        else:
            blocks = np.zeros((n_blocks, 64), dtype=np.int8)
            for i in range(n_blocks):
                if i != n_blocks - 1:
                    for j in range(64):
                        blocks[i][j] = self.plain_text[64 * i + j]
                else:
                    p = 0
                    for j in range(64 * (n_blocks - 1), size):
                        blocks[i][p] = self.plain_text[j]
                        p += 1
        return blocks

    def ECB_mode(self):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros_like(plain_blocks)
        # for i in range(n_blocks):
        for i in tqdm(range(n_blocks), desc="Encrypting"):
            encr_blocks[i] = self.encrypt_one_block(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks

    def CBC_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros((n_blocks + 1, 64), dtype=np.int8)
        encr_blocks[0] = init_vec
        for i in tqdm(range(n_blocks)):
            plain_blocks[i] = plain_blocks[i] ^ encr_blocks[i]
            encr_blocks[i + 1] = self.encrypt_one_block(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks[1:]

    def CFB_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks(init_vec)
        n_blocks = plain_blocks.shape[0] - 1
        encr_blocks = np.zeros((n_blocks, 64), dtype=np.int8)
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

# message = sts.bernoulli.rvs(0.5, size=1024)
# key = sts.bernoulli.rvs(0.5, size=64)
#
# cipher = DES_cipher()
# cipher.set_plaintext(message)
# cipher.set_cipherkey(key)
# print(cipher.OFB_mode(sts.bernoulli.rvs(0.5, size=64)))
# print(cipher.BitOutput())
