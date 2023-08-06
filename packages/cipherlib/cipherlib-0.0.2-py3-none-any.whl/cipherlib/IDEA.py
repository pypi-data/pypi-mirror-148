import numpy as np
import scipy.stats as sts
from tqdm import tqdm


class IDEA_cipher:
    def __init__(self):
        self.plain_text = None
        self.cipher_key = None
        self.cipher_text = None
        self.const_2_16 = 2 ** 16
        self.encr_blocks = None
        self.round_keys = None

    def BitOutput(self):
        out = np.zeros(64*self.encr_blocks.shape[0], dtype=np.int8)
        for i in range(self.encr_blocks.shape[0]):
            out[64*i: 64*i+64] = self.encr_blocks[i]
        return out

    def set_cipherkey(self, key):
        self.cipher_key = key
        self.KeyExpansion()

    def set_plaintext(self, PT):
        self.plain_text = PT

    def get_ciphertext(self):
        return self.cipher_text

    def ArrayToInt(self, arr):
        n = 0
        p = arr.shape[0] - 1
        for i in range(p+1):
            n += arr[i] * 2 ** p
            p -= 1
        return n

    def sum_mod(self, arr1, arr2):
        n1 = self.ArrayToInt(arr1)
        n2 = self.ArrayToInt(arr2)
        result = (n1 + n2) % self.const_2_16
        out_arr = np.zeros(16, dtype=np.int8)
        p = 15
        while result != 0:
            out_arr[p] = result % 2
            result //= 2
            p -= 1
        return out_arr

    def mult_mod(self, arr1, arr2):
        n1 = self.ArrayToInt(arr1)
        if n1 == 0:
            n1 = 65536
        n2 = self.ArrayToInt(arr2)
        if n2 == 0:
            n2 = 65536
        result = (n1 * n2) % (self.const_2_16 + 1)
        if result == 65536:
            result = 0
        out_arr = np.zeros(16, dtype=np.int8)
        p = 15
        while result != 0:
            out_arr[p] = result % 2
            result //= 2
            p -= 1
        return out_arr

    def KeyExpansion(self):
        SK = np.zeros(52, dtype=np.object)
        K = self.cipher_key.copy()
        s = 0
        for j in range(6):
            k = np.array_split(K, 8)
            for sk in k:
                SK[s] = sk
                s += 1
            K = np.roll(self.cipher_key, -25)
        k = np.array_split(self.cipher_key, 8)
        for i in range(4):
            SK[s] = k[i]
            s += 1
        self.round_keys = SK
        return 0

    def encrypt_one_block(self, plainblock):
        X = np.array_split(plainblock, 4)
        for R in range(8):
            X[0] = self.mult_mod(X[0], self.round_keys[R * 6])
            X[1] = self.sum_mod(X[1], self.round_keys[R * 6 + 1])
            X[2] = self.sum_mod(X[2], self.round_keys[R * 6 + 2])
            X[3] = self.mult_mod(X[3], self.round_keys[R * 6 + 3])
            y1 = X[0] ^ X[2]
            y2 = X[1] ^ X[3]
            y1 = self.mult_mod(y1, self.round_keys[R * 6 + 4])
            y2 = self.sum_mod(y1, y2)
            y2 = self.mult_mod(y2, self.round_keys[R * 6 + 5])
            y1 = self.sum_mod(y1, y2)
            X[0] = X[0] ^ y2
            X[2] = X[2] ^ y2
            X[1] = X[1] ^ y1
            X[3] = X[3] ^ y1
            X[1], X[2] = X[2], X[1]
        X[0] = self.mult_mod(X[0], self.round_keys[-4])
        X[1] = self.sum_mod(X[1], self.round_keys[-3])
        X[2] = self.sum_mod(X[2], self.round_keys[-2])
        X[3] = self.mult_mod(X[3], self.round_keys[-1])
        out = np.concatenate([X[0], X[1], X[2], X[3]])
        return out

    def one_round_encryption(self, plain_block, round_keys=np.array([])):
        if round_keys.size == 0:
            round_keys = sts.bernoulli.rvs(0.5, size=(6, 16))
        X = np.array_split(plain_block, 4)
        X[0] = self.mult_mod(X[0], round_keys[0])
        X[1] = self.sum_mod(X[1], round_keys[1])
        X[2] = self.sum_mod(X[2], round_keys[2])
        X[3] = self.mult_mod(X[3], round_keys[3])
        y1 = X[0] ^ X[2]
        y2 = X[1] ^ X[3]
        y1 = self.mult_mod(y1, round_keys[4])
        y2 = self.sum_mod(y1, y2)
        y2 = self.mult_mod(y2, round_keys[5])
        y1 = self.sum_mod(y1, y2)
        X[0] = X[0] ^ y2
        X[2] = X[2] ^ y2
        X[1] = X[1] ^ y1
        X[3] = X[3] ^ y1
        X[1], X[2] = X[2], X[1]
        return X[0], X[1], X[2], X[3]

    def ArrayToBlocks(self, init_vec=np.array([])):
        size = self.plain_text.shape[0]
        if 0 < size/64-int(size/64) <= 0.5:
            n_blocks = int(size/64+1)
        elif 0.5 < size/64-int(size/64) < 1:
            n_blocks = int(size/64) + 1
        else:
            n_blocks = size//64
        if init_vec.size != 0:
            blocks = np.zeros((n_blocks+1, 64), dtype=np.int8)
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
        for i in tqdm(range(n_blocks)):
            encr_blocks[i] = self.encrypt_one_block(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks

    def CBC_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros((n_blocks+1, 64), dtype=np.int8)
        encr_blocks[0] = init_vec
        for i in tqdm(range(n_blocks)):
            plain_blocks[i] = plain_blocks[i] ^ encr_blocks[i]
            encr_blocks[i+1] = self.encrypt_one_block(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks[1:]

    def CFB_mode(self, init_vec):
        plain_blocks = self.ArrayToBlocks(init_vec)
        n_blocks = plain_blocks.shape[0]-1
        encr_blocks = np.zeros((n_blocks, 64), dtype=np.int8)
        first_block = self.encrypt_one_block(plain_blocks[0]) ^ plain_blocks[1]
        encr_blocks[0] = first_block
        for i in tqdm(range(1, n_blocks)):
            encr_blocks[i] = self.encrypt_one_block(encr_blocks[i-1]) ^ plain_blocks[i+1]
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
            temp[i] = self.encrypt_one_block(temp[i-1])
            encr_blocks[i] = temp[i] ^ plain_blocks[i]
        self.encr_blocks = encr_blocks
        return encr_blocks


# plaintext = sts.bernoulli.rvs(0.5, size=512)
# cipher_key = sts.bernoulli.rvs(0.5, size=128)
#
# cipher = IDEA_cipher()
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipher_key)
# cipher.OFB_mode(sts.bernoulli.rvs(0.5, size=64))
# print(cipher.BitOutput())
# print(cipher.one_round_encryption(sts.bernoulli.rvs(0.5, size=64)))
