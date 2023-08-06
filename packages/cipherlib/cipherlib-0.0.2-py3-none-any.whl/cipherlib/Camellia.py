import numpy as np
import scipy.stats as sts


class CamelliaCipher:
    MASK8 = 0xff
    MASK32 = 0xffffffff
    MASK64 = 0xffffffffffffffff
    MASK128 = 0xffffffffffffffffffffffffffffffff
    s_box = [[112, 130, 44, 236, 179, 39, 192, 229, 228, 133, 87, 53, 234, 12, 174, 65],
                     [35, 239, 107, 147, 69, 25, 165, 33, 237, 14, 79, 78, 29, 101, 146, 189],
                     [134, 184, 175, 143, 124, 235, 31, 206, 62, 48, 220, 95, 94, 197, 11, 26],
                     [166, 225, 57, 202, 213, 71, 93, 61, 217, 1, 90, 214, 81, 86, 108, 77],
                     [139, 13, 154, 102, 251, 204, 176, 45, 116, 18, 43, 32, 240, 177, 132, 153],
                     [223, 76, 203, 194, 52, 126, 118, 5, 109, 183, 169, 49, 209, 23, 4, 215],
                     [20, 88, 58, 97, 222, 27, 17, 28, 50, 15, 156, 22, 83, 24, 242, 34],
                     [254, 68, 207, 178, 195, 181, 122, 145, 36, 8, 232, 168, 96, 252, 105, 80],
                     [170, 208, 160, 125, 161, 137, 98, 151, 84, 91, 30, 149, 224, 255, 100, 210],
                     [16, 196, 0, 72, 163, 247, 117, 219, 138, 3, 230, 218, 9, 63, 221, 148],
                     [135, 92, 131, 2, 205, 74, 144, 51, 115, 103, 246, 243, 157, 127, 191, 226],
                     [82, 155, 216, 38, 200, 55, 198, 59, 129, 150, 111, 75, 19, 190, 99, 46],
                     [233, 121, 167, 140, 159, 110, 188, 142, 41, 245, 249, 182, 47, 253, 180, 89],
                     [120, 152, 6, 106, 231, 70, 113, 186, 212, 37, 171, 66, 136, 162, 141, 250],
                     [114, 7, 185, 85, 248, 238, 172, 10, 54, 73, 42, 104, 60, 56, 241, 164],
                     [64, 40, 211, 123, 187, 201, 67, 193, 21, 227, 173, 244, 119, 199, 128, 158]]

    def __init__(self, mode):
        self.mode = mode
        self.plain_text = None
        self.cipher_key = None
        self.k = None
        self.ke = None
        self.kw = None

    def set_plaintext(self, plain_text):
        self.plain_text = plain_text
        return 0

    def set_cipherkey(self, cipher_key):
        self.cipher_key = cipher_key
        self.KeyExpansion()
        return 0

    def left_rot(self, num, p):
        size = len(format(num, 'b'))
        for i in range(p):
            a = num >> (size - 1)
            b = num & (2**(size-1)-1)
            num = (b << 1) | a
        return int(num)

    def SubBytes(self, t, box_i):
        if box_i == 1:
            x = t >> 4
            y = t & 0xf
            box_out = self.s_box[x][y]
        elif box_i == 2:
            x = t >> 4
            y = t & 0xf
            box_out = self.left_rot(self.s_box[x][y], 1)
        elif box_i == 3:
            x = t >> 4
            y = t & 0xf
            box_out = self.left_rot(self.s_box[x][y], 7)
        else:
            rot_t = self.left_rot(t, 1)
            x = rot_t >> 4
            y = rot_t & 0xf
            box_out = self.s_box[x][y]
        return box_out


    def F(self, F_IN, KE):
        x = F_IN ^ KE
        t1 = x >> 56
        t2 = (x >> 48) & self.MASK8
        t3 = (x >> 40) & self.MASK8
        t4 = (x >> 32) & self.MASK8
        t5 = (x >> 24) & self.MASK8
        t6 = (x >> 16) & self.MASK8
        t7 = (x >> 8) & self.MASK8
        t8 = x & self.MASK8
        # t1 = SBOX1[t1]
        t1 = self.SubBytes(t1, 1)
        # t2 = SBOX2[t2]
        t2 = self.SubBytes(t2, 2)
        # t3 = SBOX3[t3]
        t3 = self.SubBytes(t3, 3)
        # t4 = SBOX4[t4]
        t4 = self.SubBytes(t4, 4)
        # t5 = SBOX2[t5]
        t5 = self.SubBytes(t5, 2)
        # t6 = SBOX3[t6]
        t6 = self.SubBytes(t6, 3)
        # t7 = SBOX4[t7]
        t7 = self.SubBytes(t7, 4)
        # t8 = SBOX1[t8]
        t8 = self.SubBytes(t8, 1)
        y1 = t1 ^ t3 ^ t4 ^ t6 ^ t7 ^ t8
        y2 = t1 ^ t2 ^ t4 ^ t5 ^ t7 ^ t8
        y3 = t1 ^ t2 ^ t3 ^ t5 ^ t6 ^ t8
        y4 = t2 ^ t3 ^ t4 ^ t5 ^ t6 ^ t7
        y5 = t1 ^ t2 ^ t6 ^ t7 ^ t8
        y6 = t2 ^ t3 ^ t5 ^ t7 ^ t8
        y7 = t3 ^ t4 ^ t5 ^ t6 ^ t8
        y8 = t1 ^ t4 ^ t5 ^ t6 ^ t7
        F_OUT = (y1 << 56) | (y2 << 48) | (y3 << 40) | (y4 << 32) | (y5 << 24) | (y6 << 16) | (y7 << 8) | y8
        assert F_OUT < 2**64
        return F_OUT

    def FL(self, FL_IN, KE):
        x1 = FL_IN >> 32
        x2 = FL_IN & self.MASK32
        k1 = KE >> 32
        k2 = KE & self.MASK32
        x2 = x2 ^ self.left_rot((x1 & k1), 1)
        x1 = x1 ^ (x2 | k2)
        FL_OUT = (x1 << 32) | x2
        assert FL_OUT < 2**64
        return FL_OUT

    def FLINV(self, FLINV_IN, KE):
        y1 = FLINV_IN >> 32
        y2 = FLINV_IN & self.MASK32
        k1 = KE >> 32
        k2 = KE & self.MASK32
        y1 = y1 ^ (y2 | k2)
        y2 = y2 ^ self.left_rot((y1 & k1), 1)
        FLINV_OUT = (y1 << 32) | y2
        return FLINV_OUT

    def KeyExpansion(self):
        Sigma1 = 0xA09E667F3BCC908B
        Sigma2 = 0xB67AE8584CAA73B2
        Sigma3 = 0xC6EF372FE94F82BE
        Sigma4 = 0x54FF53A5F1D36F1C
        Sigma5 = 0x10E527FADE682D1D
        Sigma6 = 0xB05688C2B3E6C1FD
        if self.mode == 128:
            KL = self.cipher_key
            KR = 0
        elif self.mode == 192:
            KL = self.cipher_key >> 64
            KR = ((self.cipher_key & self.MASK64) << 64) | ((self.cipher_key & self.MASK64) ^ self.MASK64)
        else:
            KL = self.cipher_key >> 128
            KR = self.cipher_key & self.MASK128

        D1 = (KL ^ KR) >> 64
        D2 = (KL ^ KR) & self.MASK64
        D2 = D2 ^ self.F(D1, Sigma1)
        D1 = D1 ^ self.F(D2, Sigma2)
        D1 = D1 ^ (KL >> 64)
        D2 = D2 ^ (KL & self.MASK64)
        D2 = D2 ^ self.F(D1, Sigma3)
        D1 = D1 ^ self.F(D2, Sigma4)
        KA = (D1 << 64) | D2
        D1 = (KA ^ KR) >> 64
        D2 = (KA ^ KR) & self.MASK64
        D2 = D2 ^ self.F(D1, Sigma5)
        D1 = D1 ^ self.F(D2, Sigma6)
        KB = (D1 << 64) | D2

        if self.mode == 128:
            kw = [0] * 4
            ke = [0] * 4
            k = [0] * 18
            # kw1 = (KL << < 0) >> 64;
            kw[0] = self.left_rot(KL, 0) >> 64
            # kw2 = (KL << < 0) & MASK64;
            kw[1] = self.left_rot(KL, 0) & self.MASK64
            # k1 = (KA << < 0) >> 64;
            k[0] = self.left_rot(KA, 0) >> 64
            # k2 = (KA << < 0) & MASK64;
            k[1] = self.left_rot(KA, 0) & self.MASK64
            # k3 = (KL << < 15) >> 64;
            k[2] = self.left_rot(KL, 15) >> 64
            # k4 = (KL << < 15) & MASK64;
            k[3] = self.left_rot(KL, 15) & self.MASK64
            # k5 = (KA << < 15) >> 64;
            k[4] = self.left_rot(KA, 15) >> 64
            # k6 = (KA << < 15) & MASK64;
            k[5] = self.left_rot(KA, 15) & self.MASK64
            # ke1 = (KA << < 30) >> 64;
            ke[0] = self.left_rot(KA, 30) >> 64
            # ke2 = (KA << < 30) & MASK64;
            ke[1] = self.left_rot(KA, 30) & self.MASK64
            # k7 = (KL << < 45) >> 64;
            k[6] = self.left_rot(KL, 45) >> 64
            # k8 = (KL << < 45) & MASK64;
            k[7] = self.left_rot(KL, 45) & self.MASK64
            # k9 = (KA << < 45) >> 64;
            k[8] = self.left_rot(KA, 45) >> 64
            # k10 = (KL << < 60) & MASK64;
            k[9] = self.left_rot(KL, 60) & self.MASK64
            # k11 = (KA << < 60) >> 64;
            k[10] = self.left_rot(KA, 60) >> 64
            # k12 = (KA << < 60) & MASK64;
            k[11] = self.left_rot(KA, 60) & self.MASK64
            # ke3 = (KL << < 77) >> 64;
            ke[2] = self.left_rot(KL, 77) >> 64
            # ke4 = (KL << < 77) & MASK64;
            ke[3] = self.left_rot(KL, 77) & self.MASK64
            # k13 = (KL << < 94) >> 64;
            k[12] = self.left_rot(KL, 94) >> 64
            # k14 = (KL << < 94) & MASK64;
            k[13] = self.left_rot(KL, 94) & self.MASK64
            # k15 = (KA << < 94) >> 64;
            k[14] = self.left_rot(KA, 94) >> 64
            # k16 = (KA << < 94) & MASK64;
            k[15] = self.left_rot(KA, 94) & self.MASK64
            # k17 = (KL << < 111) >> 64;
            k[16] = self.left_rot(KL, 111) >> 64
            # k18 = (KL << < 111) & MASK64;
            k[17] = self.left_rot(KL, 111) & self.MASK64
            # kw3 = (KA << < 111) >> 64;
            kw[2] = self.left_rot(KA, 111) >> 64
            # kw4 = (KA << < 111) & MASK64;
            kw[3] = self.left_rot(KA, 111) & self.MASK64

        else:
            kw = [0] * 4
            k = [0] * 24
            ke = [0] * 6
            # kw1 = (KL << < 0) >> 64;
            kw[0] = self.left_rot(KL, 0) >> 64
            # kw2 = (KL << < 0) & MASK64;
            kw[1] = self.left_rot(KL, 0) & self.MASK64
            # k1 = (KB << < 0) >> 64;
            k[0] = self.left_rot(KB, 0) >> 64
            # k2 = (KB << < 0) & MASK64;
            k[1] = self.left_rot(KB, 0) & self.MASK64
            # k3 = (KR << < 15) >> 64;
            k[2] = self.left_rot(KR, 15) >> 64
            # k4 = (KR << < 15) & MASK64;
            k[3] = self.left_rot(KR, 15) & self.MASK64
            # k5 = (KA << < 15) >> 64;
            k[4] = self.left_rot(KA, 15) >> 64
            # k6 = (KA << < 15) & MASK64;
            k[5] = self.left_rot(KA, 15) & self.MASK64
            # ke1 = (KR << < 30) >> 64;
            ke[1] = self.left_rot(KR, 30) >> 64
            # ke2 = (KR << < 30) & MASK64;
            ke[2] = self.left_rot(KR, 30) & self.MASK64
            # k7 = (KB << < 30) >> 64;
            k[6] = self.left_rot(KB, 30) >> 64
            # k8 = (KB << < 30) & MASK64;
            k[7] = self.left_rot(KB, 30) & self.MASK64
            # k9 = (KL << < 45) >> 64;
            k[8] = self.left_rot(KL, 45) >> 64
            # k10 = (KL << < 45) & MASK64;
            k[9] = self.left_rot(KL, 45) & self.MASK64
            # k11 = (KA << < 45) >> 64;
            k[10] = self.left_rot(KA, 45) >> 64
            # k12 = (KA << < 45) & MASK64;
            k[11] = self.left_rot(KA, 45) & self.MASK64
            # ke3 = (KL << < 60) >> 64;
            ke[2] = self.left_rot(KL, 60) >> 64
            # ke4 = (KL << < 60) & MASK64;
            ke[3] = self.left_rot(KL, 60) & self.MASK64
            # k13 = (KR << < 60) >> 64;
            k[12] = self.left_rot(KR, 60) >> 64
            # k14 = (KR << < 60) & MASK64;
            k[13] = self.left_rot(KR, 60) & self.MASK64
            # k15 = (KB << < 60) >> 64;
            k[14] = self.left_rot(KB, 60) >> 60
            # k16 = (KB << < 60) & MASK64;
            k[15] = self.left_rot(KB, 60) & self.MASK64
            # k17 = (KL << < 77) >> 64;
            k[16] = self.left_rot(KL, 77) >> 64
            # k18 = (KL << < 77) & MASK64;
            k[17] = self.left_rot(KL, 77) & self.MASK64
            # ke5 = (KA << < 77) >> 64;
            ke[4] = self.left_rot(KA, 77) >> 64
            # ke6 = (KA << < 77) & MASK64;
            ke[5] = self.left_rot(KA, 77) & self.MASK64
            # k19 = (KR << < 94) >> 64;
            k[18] = self.left_rot(KR, 94) >> 64
            # k20 = (KR << < 94) & MASK64;
            k[19] = self.left_rot(KR, 94) & self.MASK64
            # k21 = (KA << < 94) >> 64;
            k[20] = self.left_rot(KA, 94) >> 64
            # k22 = (KA << < 94) & MASK64;
            k[21] = self.left_rot(KA, 94) & self.MASK64
            # k23 = (KL << < 111) >> 64;
            k[22] = self.left_rot(KL, 111) >> 64
            # k24 = (KL << < 111) & MASK64;
            k[23] = self.left_rot(KL, 111) & self.MASK64
            # kw3 = (KB << < 111) >> 64;
            kw[2] = self.left_rot(KB, 111) >> 64
            # kw4 = (KB << < 111) & MASK64;
            kw[3] = self.left_rot(KB, 111) & self.MASK64

        self.k = k
        self.ke = ke
        self.kw = kw
        return 0

    def _encrypt_one_block128(self, plain_block):
        D1 = plain_block >> 64
        D2 = plain_block & self.MASK64
        D1 = D1 ^ self.kw[0]
        D2 = D2 ^ self.kw[1]
        D2 = D2 ^ self.F(D1, self.k[0])
        D1 = D1 ^ self.F(D2, self.k[1])
        D2 = D2 ^ self.F(D1, self.k[2])
        D1 = D1 ^ self.F(D2, self.k[3])
        D2 = D2 ^ self.F(D1, self.k[4])
        D1 = D1 ^ self.F(D2, self.k[5])
        D1 = self.FL(D1, self.ke[0])
        D2 = self.FLINV(D2, self.ke[1])
        D2 = D2 ^ self.F(D1, self.k[6])
        D1 = D1 ^ self.F(D2, self.k[7])
        D2 = D2 ^ self.F(D1, self.k[8])
        D1 = D1 ^ self.F(D2, self.k[9])
        D2 = D2 ^ self.F(D1, self.k[10])
        D1 = D1 ^ self.F(D2, self.k[11])
        D1 = self.FL(D1, self.ke[2])
        D2 = self.FLINV(D2, self.ke[3])
        D2 = D2 ^ self.F(D1, self.k[12])
        D1 = D1 ^ self.F(D2, self.k[13])
        D2 = D2 ^ self.F(D1, self.k[14])
        D1 = D1 ^ self.F(D2, self.k[15])
        D2 = D2 ^ self.F(D1, self.k[16])
        D1 = D1 ^ self.F(D2, self.k[17])
        D2 = D2 ^ self.kw[2]
        D1 = D1 ^ self.kw[3]
        C = (D2 << 64) | D1
        return C

    def _encrypt_one_block192_256(self, plain_block):
        D1 = plain_block >> 64
        D2 = plain_block & self.MASK64
        D1 = D1 ^ self.kw[0]
        D2 = D2 ^ self.kw[1]
        D2 = D2 ^ self.F(D1, self.k[0])
        D1 = D1 ^ self.F(D2, self.k[1])
        D2 = D2 ^ self.F(D1, self.k[2])
        D1 = D1 ^ self.F(D2, self.k[3])
        D2 = D2 ^ self.F(D1, self.k[4])
        D1 = D1 ^ self.F(D2, self.k[5])
        D1 = self.FL(D1, self.ke[0])
        D2 = self.FLINV(D2, self.ke[1])
        D2 = D2 ^ self.F(D1, self.k[6])
        D1 = D1 ^ self.F(D2, self.k[7])
        D2 = D2 ^ self.F(D1, self.k[8])
        D1 = D1 ^ self.F(D2, self.k[9])
        D2 = D2 ^ self.F(D1, self.k[10])
        D1 = D1 ^ self.F(D2, self.k[11])
        D1 = self.FL(D1, self.ke[2])
        D2 = self.FLINV(D2, self.ke[3])
        D2 = D2 ^ self.F(D1, self.k[12])
        D1 = D1 ^ self.F(D2, self.k[13])
        D2 = D2 ^ self.F(D1, self.k[14])
        D1 = D1 ^ self.F(D2, self.k[15])
        D2 = D2 ^ self.F(D1, self.k[16])
        D1 = D1 ^ self.F(D2, self.k[17])
        D1 = self.FL(D1, self.ke[4])
        D2 = self.FLINV(D2, self.ke[5])
        D2 = D2 ^ self.F(D1, self.k[18])
        D1 = D1 ^ self.F(D2, self.k[19])
        D2 = D2 ^ self.F(D1, self.k[20])
        D1 = D1 ^ self.F(D2, self.k[21])
        D2 = D2 ^ self.F(D1, self.k[22])
        D1 = D1 ^ self.F(D2, self.k[23])
        D2 = D2 ^ self.kw[2]
        D1 = D1 ^ self.kw[3]
        C = (D2 << 64) | D1
        return C

    def encrypt_one_block(self, plain_block):
        if self.mode == 128:
            encr_block = self._encrypt_one_block128(plain_block)
        else:
            encr_block = self._encrypt_one_block192_256(plain_block)
        return encr_block

# cipher = CamelliaCipher(128)
# cipher.set_plaintext(0x0123456789abcdeffedcba9876543210)
# cipher.set_cipherkey(0x0123456789abcdeffedcba9876543210)
# print(cipher.encrypt_one_block(0x0123456789abcdeffedcba9876543210))
