#from math import sqrt
from random import randint

# ==== RSA auth block =====
class HashGen(object):
    @staticmethod
    def gen_hash(msg:str) -> int:
        # generating super dummy hash digest
        return 17

class RSAUserA(object):
    def __init__(self, msg):
        self.__msg = msg

    def generate_keys(self):
        self.__open_key = (5, 91) # dummy generetion of open key (e,n)
        print('User A: generated open key ({}, {})'.format(self.__open_key[0], self.__open_key[1]))
        self.__private_key = 29   # also
        print('User A: generated private key ({})'.format(self.__private_key))
        return self.__open_key
        
    def calculate_signature(self):
        # generating message digest
        h = HashGen.gen_hash(self.__msg)
        print('User A: generated digest h ({})'.format(h))
        # calculating signature
        self.__sign = (h ** self.__private_key) % self.__open_key[1] 
        
    def send_msg_and_signature(self) -> tuple:
        print('User A: sent a digest signature to user B')
        return self.__msg, self.__sign


class RSAUserB(object):
    def check_user_signature(self, user_a: RSAUserA):
        open_key = user_a.generate_keys()
        user_a.calculate_signature()
        msg, sign = user_a.send_msg_and_signature()
        msg_h = HashGen.gen_hash(msg)
        print('User B: calculated msg digest ({})'.format(msg_h))
        sign_h = (sign ** open_key[0]) % open_key[1]
        print('User B: calculated digest based on user A\'s signature ({})'.format(sign_h))
        if sign_h == msg_h:
            print('User B: claimed that msg was sent by user A')
        else:
            print('User B: seems like msg was NOT sent by user A')


def try_RSA_signature():
    user_a = RSAUserA('Dummy message...')
    user_b = RSAUserB()
    user_b.check_user_signature(user_a)

# ==== Standart 34.10-94 signature block ====
class ShnorUserA(object):
    def __init__(self, msg):
        self.__msg = msg

    def generate_keys(self) -> tuple:
        self.__p, self.__q = 79,13
        self.__a = 2
        while((self.__a ** self.__q) % self.__p != 1):
            self.__a += 1
        if self.__a >= self.__p - 1:
            self.__p = self.__a + 2
        print('User A: generated simple nums (p,q) ({},{})'.format(self.__p, self.__q))
        print('User A: generated num a ({})'.format(self.__a))
        self.__x = randint(1, self.__q-1)
        print('User A: generated secret key x ({})'.format(self.__x))
        self.__y = (self.__a ** self.__x) % self.__p
        print('User A: generated open key y ({})'.format(self.__y))
        return self.__p, self.__q, self.__a, self.__y
        
    def calculate_signature(self):
        h = HashGen.gen_hash(self.__msg)
        print('User A: generated msg digest ({})'.format(h))
        success_gen = False
        while(not success_gen):
            k = randint(1, self.__q-1)
            w1 = (self.__a ** k) % self.__p
            self.__w2 = w1 % self.__q
            if self.__w2 == 0:
                continue
            self.__s = ((self.__x * self.__w2) + (k * h)) % self.__q
            if self.__s == 0:
                continue
            success_gen = True
            print('User A: chose k ({})'.format(k))
            print('User A: calculated w\' ({})'.format(self.__w2))
            print('User A: calculated signature s ({})'.format(self.__s))

    def send_msg_and_sign(self) -> tuple:
        print('User A: sent msg and signature to User B')
        return self.__msg, self.__w2, self.__s


class ShnorUserB(object):
    def check_user_signature(self, user_a: ShnorUserA):
        p, q, a, y = user_a.generate_keys()
        user_a.calculate_signature()
        msg, w2, s = user_a.send_msg_and_sign()
        h = HashGen.gen_hash(msg)
        print('User B: calculated msg digest ({})'.format(h))
        v = (h ** (q-2)) % q
        print('User B: calculated v ({})'.format(v))
        z1 = (s * v) % q
        z2 = ((q - w2) * v) % q
        print('User B: calculated z1, z2 ({},{})'.format(z1, z2))
        u = (((a ** z1) * (y ** z2)) % p) % q
        print('User B: calculated u ({})'.format(u))
        if u == w2:
            print('User B: claimed that msg was sent by user A')
        else:
            print('User B: seems like msg was NOT sent by user A')


def try_Shnor_signature():
    user_a = ShnorUserA('Dummy message...')
    user_b = ShnorUserB()
    user_b.check_user_signature(user_a)

# ======== Standart 34.10-2001 signature block ============

class Standart34UserA(object):
    def __init__(self, msg:str):
        self.__msg = msg
    
    def generate_keys(self):
        self.__n = 41
        self.__A = 3
        self.__B = 7
        self.__xp = 7
        self.__yp = 17
        self.__q = 47
        self.__d = 10
        self.__xq = 36
        self.__yq = 20
        return self.__A, self.__B, (self.__xp, self.__yp), self.__n, (self.__xq, self.__yq), self.__q

    def calculate_sign(self):
        h = 7#HashGen.gen_hash(self.__msg)
        print('User A: generated digest ({})'.format(h))
        e = h % self.__q
        print('User A: calculated e ({})'.format(e))
        k = 11#randint(1, self.__q - 1)
        print('User A: generated k ({})'.format(k))
        cx, cy = Standart34UserA.multiply_point((self.__xp, self.__yp), k, self.__A)
        print('User A: calculated C(x,y) ({},{})'.format(cx, cy))
        self.__r = int(cx) % self.__q
        print('User A: calculated r ({})'.format(self.__r))
        self.__s = (self.__r * self.__d + k * e) % self.__q
        print('User A: calculated s ({})'.format(self.__s))

    def send_msg_and_sign(self):
        return self.__msg, self.__r, self.__s
      
    @staticmethod
    def multiply_point(p:tuple, n:int, A:int) -> tuple:
        pk = None
        q = p
        for i in range(len(bin(n))-2):
            if n and (1 << i) == (1 << i):
                if pk == None:
                    pk = q
                else:
                    pk =  Standart34UserA.add_points(pk, q, A)
            q =  Standart34UserA.add_points(q, q, A)
        return pk

    @staticmethod
    def add_points(p1:tuple, p2:tuple, A:int) -> tuple:
        if p1[0] != p2[0]:
            k = (p2[1] - p1[1]) / (p2[0] - p1[0])
        else:
            k = (3 * p1[0]**2 + A) / (2 * p1[1])
        x3 = k**2 - p1[0] - p2[0]
        y3 = k * (p1[0] - x3) - p1[1]
        return (x3, y3)

class Standart34UserB(object):
    def check_user_signature(self, user_a: Standart34UserA):
        A, B, P, n, Q, q = user_a.generate_keys()
        user_a.calculate_sign()
        msg, r, s = user_a.send_msg_and_sign()
        h = 7#HashGen.gen_hash(msg)
        print('User B: generated msg digest ({})'.format(h))
        e = h % q
        print('User B: calculated e\' ({})'.format(e))
        e_reverse = Standart34UserB.xgcd(q, e)[2]
        if e_reverse < 0:
            e_reverse += q
        v = e_reverse % q
        print('User B: calculated v ({})'.format(v))
        z1 = (s * v) % q
        z2 = ((q - r) * v) % q 
        print('User B: calculated (z1,z2) ({}, {})'.format(z1,z2))
        c = Standart34UserA.add_points(Standart34UserA.multiply_point(P, z1, A), Standart34UserA.multiply_point(Q, z2, A), A)
        print('User B: calculated C\'(x,y) ({}, {})'.format(c[0], c[1]))
        r2 = c[0] % q
        print('User B: calculated r\' ({})'.format(r2))
        if r2 == r:
            print('User B: claimed that msg was sent by user A')
        else:
            print('User B: seems like msg was NOT sent by user A')


    @staticmethod
    def xgcd(a, b):
        """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            q, b, a = b // a, a, b % a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0


def try_standart34_10_2001():
    user_a = Standart34UserA('Dummy message...')
    user_b = Standart34UserB()  
    user_b.check_user_signature(user_a)

if __name__ == '__main__':
    print('======== RSA based signature ========')
    try_RSA_signature()
    print('======== Standart 34.10-94 based signature =========')
    try_Shnor_signature()
    print('======== Standart 34.10-2001 based signature =========')
    try_standart34_10_2001()
