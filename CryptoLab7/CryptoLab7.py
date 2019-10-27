# algorithm is according to https://www.ietf.org/rfc/rfc1321.txt

from math import sin, floor
from bitarray import bitarray

class MD5_Buffers(object):
        def __init__(self):
            self.A = 0x67452301
            self.B = 0xEFCDAB89
            self.C = 0x98BADCFE
            self.D = 0x10325476

        def init(self):
            self.__init__()


class MD5_Hasher(object):
    def __init__(self):
        self.__msg = None
        self.__buffers = MD5_Buffers()
        # variable for my personal report
        self.__debug_on = True

    def hash_msg(self, message: str) -> str:
        self.__msg = message
        self.__step_1()
        self.__step_2()
        self.__step_3()
        self.__step_4()
        return self.__step_5()

    def __step_1(self):
        # padding the message
        self.__bits = bitarray()
        # each encoded byte to bits
        if self.__debug_on:
            print('The message in win1251 codes:')
        for char in self.__msg:
            self.__bits.frombytes(char.encode('cp1251'))
            if self.__debug_on:
                print(int.from_bytes(char.encode('cp1251'), 'little'), end=' ')
        if self.__debug_on:
            print()
        self.__bits_len = self.__bits.length()
        # append first padding bit
        self.__bits.append(True)
        while self.__bits.length() % 512 != 448:
            self.__bits.append(False) 
       
    def __step_2(self):
        # adding length in 64 bits to message
        if self.__bits_len > 2**64 - 1:
            self.__bits_len = self.__bits_len & 0xFFFFFFFFFFFFFFFF
        # writing length of the message
        # These bits are appended as two 32-bit words and appended LOW-ORDER WORD FIRST in accordance with rfc
        self.__bits.frombytes((self.__bits_len & 0xFFFFFFFF).to_bytes(4, byteorder='little'))
        self.__bits.frombytes(((self.__bits_len & 0xFFFFFFFF00000000) >> 32).to_bytes(4, byteorder='little'))    
        # some notes from rfc:
        # a "word" is a 32-bit quantity;
        # a sequence of bytes can be interpreted as a sequence of 32-bit words, where each
        # consecutive group of four bytes is interpreted as a word with the
        # LOW-ORDER (least significant) BYTE GIVEN FIRST. 
        # (That's why i used 'little' as byteorder)
        if self.__debug_on:
            print(self.__bits)
                    
    def __step_3(self): 
        # initialize buffers with right values
        self.__buffers.init()

    def __step_4(self):
        # define auxilary functions
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)

        # define the left rotation function, which rotates x left n bits
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

        # Define a function for modular addition.
        modular_add = lambda a, b: (a + b) % pow(2, 32)

        hex_debug = lambda x: "{0:#0{1}x}".format(x,10)

        # define 64 element T table constructed from sine function 
        T = [floor(pow(2, 32) * abs(sin(i))) for i in range(1,65)]

        # process each 16-word (16x32 = 512) block       
        for i in range(self.__bits.length() // 512):
            # move each word to X
            X = [ self.__bits[i*512 + j*32 : i*512 + j*32 + 32] for j in range(16) ]
            # Convert the bitarray objects to integers.
            X = [int.from_bytes(word.tobytes(), byteorder='little') for word in X]
            
            A = self.__buffers.A
            B = self.__buffers.B
            C = self.__buffers.C
            D = self.__buffers.D

            for i in range(64):
                if self.__debug_on:
                     print('before_iteration_' + str(i+1),hex_debug(A),hex_debug(B),hex_debug(C),hex_debug(D),sep=' ',end=' ')

                if i < 16:
                    k = i
                    s = [7, 12, 17, 22]
                    temp = F(B, C, D)
                elif 16 <= i < 32:
                    k = ((5 * i) + 1) % 16
                    s = [5, 9, 14, 20]
                    temp = G(B, C, D)
                elif 32 <= i < 48:
                    k = ((3 * i) + 5) % 16
                    s = [4, 11, 16, 23]
                    temp = H(B, C, D)
                elif 48 <= i < 64:
                    k = (7 * i) % 16
                    s = [6, 10, 15, 21]
                    temp = I(B, C, D)

                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = modular_add(temp, A)
                temp = rotate_left(temp, s[i % 4])
                temp = modular_add(temp, B)
           
                # Swap the registers for the next operation.
                A = D
                D = C
                C = B
                B = temp

                if self.__debug_on:
                     print('after__iteration_' + str(i+1),hex_debug(A),hex_debug(B),hex_debug(C),hex_debug(D),sep=' ')

            # Update the buffers with the results
            self.__buffers.A = modular_add(self.__buffers.A, A)
            self.__buffers.B = modular_add(self.__buffers.B, B)
            self.__buffers.C = modular_add(self.__buffers.C, C)
            self.__buffers.D = modular_add(self.__buffers.D, D)

    def __step_5(self) -> str:
        hex = lambda x: "{0:#0{1}x}".format(x,10)

        if self.__debug_on:
            print('before bytes swap ', 'A = ' + hex(self.__buffers.A), 'B = ' + hex(self.__buffers.B), 'C = ' + hex(self.__buffers.C), 'D = ' + hex(self.__buffers.D),sep=' ')
        A = MD5_Hasher.__change_endianess_32(self.__buffers.A)
        B = MD5_Hasher.__change_endianess_32(self.__buffers.B)
        C = MD5_Hasher.__change_endianess_32(self.__buffers.C)
        D = MD5_Hasher.__change_endianess_32(self.__buffers.D)
        if self.__debug_on:
            print(' after bytes swap ', 'A = ' + hex(A), 'B = ' + hex(B), 'C = ' + hex(C), 'D = ' + hex(D),sep=' ')

        hex = lambda x: "{0:#0{1}x}".format(x, 34)
        return hex((A << 3 * 32) + (B << 2 * 32) + (C << 32) + D)  

    @staticmethod
    def __change_endianess_32(x) -> int:
        return int.from_bytes(x.to_bytes(4, byteorder='little'), byteorder='big', signed=False)



if __name__ == '__main__':
    print('=========== MD5 hasher ==========')
    print('Please, enter the message, that you want to encode:')
    msg = input()

    hasher = MD5_Hasher()
    hashed = hasher.hash_msg(msg)
    print('Hashed message is:' + hashed)
