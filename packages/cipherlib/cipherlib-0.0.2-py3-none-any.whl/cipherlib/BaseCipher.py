import numpy as np
from tqdm import tqdm


class BaseCipher:
    def __init__(self, bytes_per_block=8):
        self.plain_text = None
        self.cipher_key = None
        self.iv = None
        self.encr_blocks = None

        # self.encrypt = None

        self.bytes_per_block = bytes_per_block

    def _set_plaintext(self, plaint_text):
        self.plain_text = plaint_text

    def _set_cipherkey(self, key):
        self.cipher_key = key

    def set_plaintext_hex(self, hex_array):
        pass

    def set_plaintext_bin(self, bin_array):
        pass

    def set_key_hex(self, hex_array):
        pass

    def set_key_bin(self, bin_array):
        pass

    def set_iv_hex(self, hex_array):
        pass

    def set_iv_bin(self, bin_array):
        pass

    def BitOutput(self):
        byte_arr = self.encr_blocks.copy()
        bit_arr = np.zeros(self.bytes_per_block * 8 * byte_arr.shape[0], dtype=np.uint8)
        for j in range(byte_arr.shape[0]):
            for i in range(byte_arr.shape[1]):
                one_byte = byte_arr[j][i]
                bit8 = bit_arr[self.bytes_per_block * 8 * j + 8 * i: self.bytes_per_block * 8 * j + 8 * i + 8]
                p = 7
                while one_byte != 0:
                    bit8[p] = one_byte % 2
                    one_byte //= 2
                    p -= 1
        return bit_arr

    def ArrayToBlocks(self, init_vec=np.array([])):
        size = self.plain_text.shape[0]
        if 0 < size / self.bytes_per_block - int(size / self.bytes_per_block) <= 0.5:
            n_blocks = int(size / self.bytes_per_block + 1)
        elif 0.5 < size / self.bytes_per_block - int(size / self.bytes_per_block) < 1:
            n_blocks = int(size / self.bytes_per_block) + 1
        else:
            n_blocks = size // self.bytes_per_block
        if init_vec.size != 0:
            blocks = np.zeros((n_blocks + 1, self.bytes_per_block), dtype=np.uint8)
            blocks[0] = init_vec
            for i in range(1, n_blocks):
                if i != n_blocks - 1:
                    for j in range(self.bytes_per_block):
                        blocks[i][j] = self.plain_text[self.bytes_per_block * i + j]
                else:
                    p = 0
                    for j in range(self.bytes_per_block * (n_blocks - 1), size):
                        blocks[i][p] = self.plain_text[j]
                        p += 1
        else:
            blocks = np.zeros((n_blocks, self.bytes_per_block), dtype=np.uint8)
            for i in range(n_blocks):
                if i != n_blocks - 1:
                    for j in range(self.bytes_per_block):
                        blocks[i][j] = self.plain_text[self.bytes_per_block * i + j]
                else:
                    p = 0
                    for j in range(self.bytes_per_block * (n_blocks - 1), size):
                        blocks[i][p] = self.plain_text[j]
                        p += 1
        return blocks

    def ECB_mode(self):
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros_like(plain_blocks)
        for i in tqdm(range(n_blocks), desc='Encrypting'):
            encr_blocks[i] = self.encrypt(plain_blocks[i])
        self.encr_blocks = encr_blocks
        return encr_blocks

    def CBC_mode(self):
        init_vec = self.iv.astype(np.uint8)
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros((n_blocks + 1, 16), dtype=np.uint8)
        encr_blocks[0] = init_vec
        for i in tqdm(range(n_blocks)):
            plain_blocks[i] = plain_blocks[i] ^ encr_blocks[i]
            encr_blocks[i + 1] = self.encrypt(plain_blocks[i])
        self.encr_blocks = encr_blocks[1:]
        return encr_blocks[1:]

    def CFB_mode(self):
        init_vec = self.iv
        plain_blocks = self.ArrayToBlocks(init_vec)
        n_blocks = plain_blocks.shape[0] - 1
        encr_blocks = np.zeros((n_blocks, 16), dtype=np.uint8)
        first_block = self.encrypt(plain_blocks[0]) ^ plain_blocks[1]
        encr_blocks[0] = first_block
        for i in tqdm(range(1, n_blocks)):
            encr_blocks[i] = self.encrypt(encr_blocks[i - 1]) ^ plain_blocks[i + 1]
        self.encr_blocks = encr_blocks
        return encr_blocks

    def OFB_mode(self):
        init_vec = self.iv
        plain_blocks = self.ArrayToBlocks()
        n_blocks = plain_blocks.shape[0]
        encr_blocks = np.zeros_like(plain_blocks)
        temp = np.zeros_like(plain_blocks)
        temp[0] = self.encrypt(init_vec)
        encr_blocks[0] = temp[0] ^ plain_blocks[0]
        for i in tqdm(range(1, n_blocks)):
            temp[i] = self.encrypt(temp[i - 1])
            encr_blocks[i] = temp[i] ^ plain_blocks[i]
        self.encr_blocks = encr_blocks
        return encr_blocks
