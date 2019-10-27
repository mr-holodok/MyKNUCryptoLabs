from math import sqrt
from random import randint

# ==== RSA auth block =====
class ARSAUser(object):
    def Generate_keys(self) -> tuple:
        self.__open_key = (5, 91) # dummy generetion
        print('User A: generated open key ({}, {})'.format(self.__open_key[0], self.__open_key[1]))
        self.__private_key = 29   # also
        print('User A: generated private key ({})'.format(self.__private_key))
        print('User A: sending open key to user B')
        return self.__open_key

    def Calculate_k(self, r:int) -> int:
        k = r**self.__private_key % self.__open_key[1] 
        print('User A: calculated k ({}) and send it to user B'.format(k))
        return k


class BRSAUser(object):
    def Auth(self, a_user: ARSAUser) -> bool:
        self.__open_key = a_user.Generate_keys()
        print('User B: got open key ({}, {}) from user A'.format(self.__open_key[0], self.__open_key[1]))
        k = randint(0, self.__open_key[1]-1)
        print('User B: generated random k ({})'.format(k))
        r = k ** self.__open_key[0] % self.__open_key[1]
        print('User B: calculated r ({}) and send it to user A'.format(r))
        k_from_a_user = a_user.Calculate_k(r)
        print('User B: checking k\'s')
        return k == k_from_a_user
 

def auth_RSA():
    a_user = ARSAUser()
    b_user = BRSAUser()
    if b_user.Auth(a_user):
        print('Authentification successfull!')
    else:
        print('Authentification failed!')

# ==== Shnor auth block ====
class ShnorUserA(object):
    def Generate_keys(self) -> int:
        self.__simple_nums = (23,11)
        print('User A: generated simple nums (p,q) ({},{})'.format(self.__simple_nums[0], self.__simple_nums[1]))
        self.__private_key = 8
        print('User A: generated secret key x ({})'.format(self.__private_key))
        self.__g = 3
        print('User A: generated g ({})'.format(self.__g))
        self.__open_key = 4
        print('User A: generated open key y ({})'.format(self.__open_key))
        print('User A: published open key')
        return self.__open_key

    def Calculate_r(self) -> int:
        self.__k = randint(0, self.__simple_nums[1]-1)
        print('User A: chose random k ({})'.format(self.__k))
        r = self.__g ** self.__k % self.__simple_nums[0]
        print('User A: calculated r ({}) and sent it to user B'.format(r))
        return r

    def Calculate_s(self, e) -> tuple:
        s = (self.__k + self.__private_key * e) % self.__simple_nums[1]
        print('User A: calculated s ({}) and sent it to user B'.format(s))
        return (s, self.__g, self.__simple_nums[0])

class ShnorUserB(object):
    def Auth(self, user_a: ShnorUserA) -> bool:
        open_key = user_a.Generate_keys()
        r = user_a.Calculate_r()
        e = randint(0, (2**10)-1)
        print('User B: chose random e ({}) and sent it to user A'.format(e))
        (s,g,p) = user_a.Calculate_s(e)
        print('User B: checking equality...')
        return r == ((g**s) * (open_key**e) % p)

def auth_Shnor():
    user_a = ShnorUserA()
    user_b = ShnorUserB()
    if user_b.Auth(user_a):
        print('Authentification successfull!')
    else:
        print('Authentification failed!')

# ======== Shamir auth block ============
class ShamirMediator(object):
    def xgcd(self, a, b):
        """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            q, b, a = b // a, a, b % a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0

    def Generate_keys(self) -> tuple:
        n = 35
        print('Mediator: selected n ({})'.format(n))
        v = set()
        for i in range(1,n+1):
            elem = i**2 % n
            (g,x,y) = self.xgcd(elem, n)
            if g == 1 and x > 0:
                v.add((elem, x))
        v = list(v)
        rand = randint(1,len(v)-1)
        inv_v = v[rand][1]
        v = v[rand][0]
        print('Mediator: selected v ({}) and its inverse ({})'.format(v, inv_v))
        s = sqrt(inv_v)
        i = 1
        while (s != int(s)):
            s = sqrt(inv_v + i*n)
            i += 1
        s = int(s)
        print('Mediator: found private key s ({})'.format(s))
        return ((v, n), s)

class ShamirUserA(object):
    def get_keys(self, keys):
        self.__open_key = keys[0]
        self.__private_key = keys[1]

    def send_open_key(self) -> tuple:
        return self.__open_key

    def calculate_r(self) -> int:
        self.__r = randint(1, self.__open_key[1])
        print('User A  : chosen r ({})'.format(self.__r))
        z = self.__r ** 2 % self.__open_key[1]
        print('User A  : calculated z ({}) and sent it to user B'.format(z))
        return z

    def get_bit_and_send_respond(self, bit: int) -> int:
        if bit == 0:
            r = self.__r
        else:
            r = self.__r * self.__private_key % self.__open_key[1]
        print('User A  : got bit {} and sent value {} to user B'.format(bit,r))
        return r

class ShamirUserB(object):
    def Auth(self, user_a: ShamirUserA):
        open_key = user_a.send_open_key()
        z = user_a.calculate_r()
        bit = randint(0,1)
        print('User B  : generated bit {}'.format(bit))
        r = user_a.get_bit_and_send_respond(bit)
        print('Checking equality...')
        if bit == 0 and z == r**2 % open_key[1]:
            return True
        elif bit != 0 and z == ((r**2) * open_key[0]) % open_key[1]:
            return True
        else:
            return False


def auth_Shamir():
    mediator = ShamirMediator()
    user_a = ShamirUserA()
    user_b = ShamirUserB()
    keys = mediator.Generate_keys()
    user_a.get_keys(keys)
    if user_b.Auth(user_a):
        print('Authentification successfull!')
    else:
        print('Authentification failed!')


if __name__ == '__main__':
    print('======== RSA based auth ========')
    auth_RSA()
    print('======== Klaud Shnor based auth ========')
    auth_Shnor()
    print('======== Feyge-Fiat-Shamir based auth =========')
    auth_Shamir()
