import numpy as np


class ARIA_cipher:
    S1_box = np.array([[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
                       [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
                       [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
                       [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
                       [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
                       [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
                       [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
                       [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
                       [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
                       [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
                       [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
                       [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
                       [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
                       [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
                       [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
                       [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]])
    S1_box_inv = np.array([[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251],
                           [124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203],
                           [84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78],
                           [8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37],
                           [114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146],
                           [108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132],
                           [144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6],
                           [208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107],
                           [58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115],
                           [150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110],
                           [71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27],
                           [252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244],
                           [31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95],
                           [96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239],
                           [160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97],
                           [23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]])
    S2_box = np.array([[226, 78, 84, 252, 148, 194, 74, 204, 98, 13, 106, 70, 60, 77, 139, 209],
                       [94, 250, 100, 203, 180, 151, 190, 43, 188, 119, 46, 3, 211, 25, 89, 193],
                       [29, 6, 65, 107, 85, 240, 153, 105, 234, 156, 24, 174, 99, 223, 231, 187],
                       [0, 115, 102, 251, 150, 76, 133, 228, 58, 9, 69, 170, 15, 238, 16, 235],
                       [45, 127, 244, 41, 172, 207, 173, 145, 141, 120, 200, 149, 249, 47, 206, 205],
                       [8, 122, 136, 56, 92, 131, 42, 40, 71, 219, 184, 199, 147, 164, 18, 83],
                       [255, 135, 14, 49, 54, 33, 88, 72, 1, 142, 55, 116, 50, 202, 233, 177],
                       [183, 171, 12, 215, 196, 86, 66, 38, 7, 152, 96, 217, 182, 185, 17, 64],
                       [236, 32, 140, 189, 160, 201, 132, 4, 73, 35, 241, 79, 80, 31, 19, 220],
                       [216, 192, 158, 87, 227, 195, 123, 101, 59, 2, 143, 62, 232, 37, 146, 229],
                       [21, 221, 253, 23, 169, 191, 212, 154, 126, 197, 57, 103, 254, 118, 157, 67],
                       [167, 225, 208, 245, 104, 242, 27, 52, 112, 5, 163, 138, 213, 121, 134, 168],
                       [48, 198, 81, 75, 30, 166, 39, 246, 53, 210, 110, 36, 22, 130, 95, 218],
                       [230, 117, 162, 239, 44, 178, 28, 159, 93, 111, 128, 10, 114, 68, 155, 108],
                       [144, 11, 91, 51, 125, 90, 82, 243, 97, 161, 247, 176, 214, 63, 124, 109],
                       [237, 20, 224, 165, 61, 34, 179, 248, 137, 222, 113, 26, 175, 186, 181, 129]])
    S2_box_inv = np.array([[48, 104, 153, 27, 135, 185, 33, 120, 80, 57, 219, 225, 114, 9, 98, 60],
                           [62, 126, 94, 142, 241, 160, 204, 163, 42, 29, 251, 182, 214, 32, 196, 141],
                           [129, 101, 245, 137, 203, 157, 119, 198, 87, 67, 86, 23, 212, 64, 26, 77],
                           [192, 99, 108, 227, 183, 200, 100, 106, 83, 170, 56, 152, 12, 244, 155, 237],
                           [127, 34, 118, 175, 221, 58, 11, 88, 103, 136, 6, 195, 53,13, 1, 139],
                           [140, 194, 230, 95, 2, 36, 117, 147, 102, 30, 229, 226, 84, 216, 16, 206],
                           [122, 232, 8, 44, 18, 151, 50, 171, 180, 39, 10, 35, 223, 239, 202, 217],
                           [184, 250, 220, 49, 107, 209, 173, 25, 73, 189, 81, 150, 238, 228, 168, 65],
                           [218, 255, 205, 85, 134, 54, 190, 97, 82, 248, 187, 14, 130, 72, 105, 154],
                           [224, 71, 158, 92, 4, 75, 52, 21, 121, 38, 167, 222, 41, 174, 146, 215],
                           [132, 233, 210, 186, 93, 243, 197, 176, 191, 164, 59, 113, 68, 70, 43, 252],
                           [235, 111, 213, 246, 20, 254, 124, 112, 90, 125, 253, 47, 24, 131, 22, 165],
                           [145, 31, 5, 149, 116, 169, 193, 91, 74, 133, 109, 19, 7, 79, 78, 69],
                           [178, 15, 201, 28, 166, 188, 236, 115, 144, 123, 207, 89, 143, 161, 249, 45],
                           [242, 177, 0, 148, 55, 159, 208, 46, 156, 110, 40, 63, 128, 240, 61, 211],
                           [37, 138, 181, 231, 66, 179, 199, 234, 247, 76, 17, 51, 3, 162, 172, 96]])

    def __init__(self, N):
        assert N in (128, 192, 256)
        self.mode = N
        if N == 128:
            self.Nr = 12
            self.Nrk = 13
        elif N == 192:
            self.Nr = 14
            self.Nrk = 15
        else:
            self.Nr = 16
            self.Nrk = 17
        self.plain_text = None
        self.cipher_key = None
        self.cipher_text = None
        self.round_keys = None

    def set_cipherkey(self, key):
        self.cipher_key = key
        self.KeyExpansion()

    def set_plaintext(self, PT):
        self.plain_text = PT

    def get_ciphertext(self):
        return self.cipher_text

    def SubBytes(self, byte, n_box):
        x = byte >> 4
        y = byte & 0xf
        if n_box == '1':
            return self.S1_box[x][y]
        elif n_box == '2':
            return self.S2_box[x][y]
        elif n_box == '1_inv':
            return self.S1_box_inv[x][y]
        else:
            return self.S2_box_inv[x][y]

    def SubLayer(self, state, type):
        new_state = np.zeros(state.shape[0], dtype=int)
        if type == 1:
            for i in range(state.shape[0]):
                if i % 4 == 0:
                    new_state[i] = self.SubBytes(state[i], '1')
                elif i % 4 == 1:
                    new_state[i] = self.SubBytes(state[i], '2')
                elif i % 4 == 2:
                    new_state[i] = self.SubBytes(state[i], '1_inv')
                else:
                    new_state[i] = self.SubBytes(state[i], '2_inv')
        if type == 2:
            for i in range(state.shape[0]):
                if i % 4 == 0:
                    new_state[i] = self.SubBytes(state[i], '1_inv')
                elif i % 4 == 1:
                    new_state[i] = self.SubBytes(state[i], '2_inv')
                elif i % 4 == 2:
                    new_state[i] = self.SubBytes(state[i], '1')
                else:
                    new_state[i] = self.SubBytes(state[i], '2')
        return new_state

    def DiffLayer(self, state):
        new_state = np.zeros(state.shape[0], dtype=int)
        new_state[0] = state[3] ^ state[4] ^ state[6] ^ state[8] ^ state[9] ^ state[13] ^ state[14]
        new_state[1] = state[2] ^ state[5] ^ state[7] ^ state[8] ^ state[9] ^ state[12] ^ state[15]
        new_state[2] = state[1] ^ state[4] ^ state[6] ^ state[10] ^ state[11] ^ state[12] ^ state[15]
        new_state[3] = state[0] ^ state[5] ^ state[7] ^ state[10] ^ state[11] ^ state[13] ^ state[14]
        new_state[4] = state[0] ^ state[2] ^ state[5] ^ state[8] ^ state[11] ^ state[14] ^ state[15]
        new_state[5] = state[1] ^ state[3] ^ state[4] ^ state[9] ^ state[10] ^ state[14] ^ state[15]
        new_state[6] = state[0] ^ state[2] ^ state[7] ^ state[9] ^ state[10] ^ state[12] ^ state[13]
        new_state[7] = state[1] ^ state[3] ^ state[6] ^ state[8] ^ state[11] ^ state[12] ^ state[13]
        new_state[8] = state[0] ^ state[1] ^ state[4] ^ state[7] ^ state[10] ^ state[13] ^ state[15]
        new_state[9] = state[0] ^ state[1] ^ state[5] ^ state[6] ^ state[11] ^ state[12] ^ state[14]
        new_state[10] = state[2] ^ state[3] ^ state[5] ^ state[6] ^ state[8] ^ state[13] ^ state[15]
        new_state[11] = state[2] ^ state[3] ^ state[4] ^ state[7] ^ state[9] ^ state[12] ^ state[14]
        new_state[12] = state[1] ^ state[2] ^ state[6] ^ state[7] ^ state[9] ^ state[11] ^ state[12]
        new_state[13] = state[0] ^ state[3] ^ state[6] ^ state[7] ^ state[8] ^ state[10] ^ state[13]
        new_state[14] = state[0] ^ state[3] ^ state[4] ^ state[5] ^ state[9] ^ state[11] ^ state[14]
        new_state[15] = state[1] ^ state[2] ^ state[4] ^ state[5] ^ state[8] ^ state[10] ^ state[15]
        return new_state

    def BitToByteArray(self, bit_arr):
        byte_arr = np.zeros(bit_arr.shape[0]//8, dtype=int)
        for i in range(byte_arr.shape[0]):
            single_byte = bit_arr[8 * i: 8 * (i + 1)].copy()
            n = 0
            for p in range(8):
                n += single_byte[p] * 2 ** (7 - p)
            byte_arr[i] = n
        return byte_arr

    def ByteToBitArray(self, byte_arr):
        bit_arr = np.zeros(8*byte_arr.shape[0], dtype=int)
        for i in range(byte_arr.shape[0]):
            single_byte = byte_arr[i].copy()
            single_bit_arr = np.zeros(8, dtype=int)
            c = 7
            while single_byte != 0:
                single_bit_arr[c] = single_byte % 2
                single_byte //= 2
                c -= 1
            bit_arr[8 * i: 8 * (i + 1)] = single_bit_arr
        return bit_arr

    def print_hex_key(self, key):
        if key.shape[0] > 16:
            key = self.BitToByteArray(key)
        s = ''
        for i in range(16):
            h = format(key[i], 'x')
            if len(h) == 1:
                h = '0' + h
            s += h
        return s

    def xor(self, arr1_old, arr2_old):
        arr1 = arr1_old.copy()
        arr2 = arr2_old.copy()
        if arr1.shape[0] < 128:
            arr1 = self.ByteToBitArray(arr1)
        if arr2.shape[0] < 128:
            arr2 = self.ByteToBitArray(arr2)
        out = arr1 ^ arr2
        out = self.BitToByteArray(out)
        return out

    def F(self, state_old, round_key_old, type):
        state = state_old.copy()
        round_key = round_key_old.copy()
        if state.shape[0] > 16:
            state = self.BitToByteArray(state)
        if round_key.shape[0] > 16:
            round_key = self.BitToByteArray(round_key)
        xor_state = self.xor(state, round_key)
        print('After XOR: ', self.print_hex_key(xor_state))
        sub_state = self.SubLayer(xor_state, type)
        print('After SubLayer: ', self.print_hex_key(sub_state))
        diff_state = self.DiffLayer(sub_state)
        print('After DiffLayer: ', self.print_hex_key(diff_state))
        return diff_state

    def KeyExpansion(self):
        C1 = np.array([0x51, 0x7c, 0xc1, 0xb7, 0x27, 0x22, 0x0a, 0x94, 0xfe, 0x12, 0xab, 0xe8, 0xfa, 0x9a, 0x6e, 0xe0])
        C2 = np.array([0x6d, 0xb1, 0x4a, 0xcc, 0x9e, 0x21, 0xc8, 0x20, 0xff, 0x28, 0xb1, 0xd5, 0xef, 0x5d, 0xe2, 0xb0])
        C3 = np.array([0xdb, 0x92, 0x37, 0x1d, 0x21, 0x26, 0xe9, 0x70, 0x03, 0x24, 0x97, 0x75, 0x04, 0xe8, 0xc9, 0x0e])
        if self.mode == 128:
            CK = np.array([C1, C2, C3])
        elif self.mode == 192:
            CK = np.array([C2, C3, C1])
        else:
            CK = np.array([C3, C1, C2])
        K = np.zeros(256, dtype=int)
        key = self.ByteToBitArray(self.cipher_key.copy())
        K[:key.shape[0]] = key
        KL, KR = np.array_split(K, 2)
        W = np.zeros(4, dtype=np.object)
        W[0] = self.BitToByteArray(KL.copy())
        W[1] = self.xor(self.F(W[0], CK[0], 1), KR)
        W[2] = self.xor(self.F(W[1], CK[1], 2), W[0])
        W[3] = self.xor(self.F(W[2], CK[2], 1), W[1])
        for i in range(4):
            W[i] = self.ByteToBitArray(W[i])
            print('W[{}] = {}'.format(i, self.print_hex_key(W[i])))
        ek = np.zeros(17, dtype=np.object)
        ek[0] = W[0] ^ np.roll(W[1], 19)
        ek[1] = W[1] ^ np.roll(W[2], 19)
        ek[2] = W[2] ^ np.roll(W[3], 19)
        ek[3] = np.roll(W[0], 19) ^ W[3]
        ek[4] = W[0] ^ np.roll(W[1], 31)
        ek[5] = W[1] ^ np.roll(W[2], 31)
        ek[6] = W[2] ^ np.roll(W[3], 31)
        ek[7] = np.roll(W[0], 31) ^ W[3]
        ek[8] = W[0] ^ np.roll(W[1], -61)
        ek[9] = W[1] ^ np.roll(W[2], -61)
        ek[10] = W[2] ^ np.roll(W[3], -61)
        ek[11] = np.roll(W[0], -61) ^ W[3]
        ek[12] = W[0] ^ np.roll(W[1], -31)
        ek[13] = W[1] ^ np.roll(W[2], -31)
        ek[14] = W[2] ^ np.roll(W[3], -31)
        ek[15] = np.roll(W[0], -31) ^ W[3]
        ek[16] = W[0] ^ np.roll(W[1], -19)
        for i in range(17):
            ek[i] = self.BitToByteArray(ek[i].copy())
        self.round_keys = ek
        return 0

    def encrypt(self):
        state = self.plain_text
        for R in range(self.Nr-1):
            if R % 2 == 0:
                state = self.F(state, self.round_keys[R], 1)
            else:
                state = self.F(state, self.round_keys[R], 2)
        state = self.SubLayer(state ^ self.round_keys[self.Nr-1], 2) ^ self.round_keys[self.Nr]
        self.cipher_text = state
        return 0


### Test 128-bit ###
# cipher = ARIA_cipher(192)
# plaintext = np.array([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
# # cipher_key = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f])
# cipher_key = np.array([0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
#                        0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17])
# cipher.set_plaintext(plaintext)
# cipher.set_cipherkey(cipher_key)
# cipher.encrypt()
# print('Cipher_text: ', cipher.print_hex_key(cipher.get_ciphertext()))
# for i, key in enumerate(cipher.round_keys):
#     print('Key {}: {}'.format(i, cipher.print_hex_key(key)))
