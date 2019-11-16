import rsa_generation
from random import randint

# ======= secret multiside calcs (RSA-based) ========

def rsa_calc_avg(s1_val:int, s2_val:int, s3_val:int) -> int:
    # each side keypairs
    s1_public, s1_private = rsa_generation.generate_keypair() 
    print("1st side has keys: public " + str(s1_public) + ' private ' + str(s1_private))
    s2_public, s2_private = rsa_generation.generate_keypair() 
    print("2nd side has keys: public " + str(s2_public) + ' private ' + str(s2_private))
    s3_public, s3_private = rsa_generation.generate_keypair() 
    print("3rd side has keys: public " + str(s3_public) + ' private ' + str(s3_private))

    # secret num
    x = randint(0, 1000)
    print('Generated secret num x {}'.format(x))

    res = rsa_generation.encrypt(s2_public, x + s3_val)
    print('3rd side encrypted val {} to {} and sent it to 2nd side'.format(x+s3_val, res))
    
    res = rsa_generation.encrypt(s1_public, rsa_generation.decrypt(s2_private, res) + s2_val)
    print('2nd side decrypted val from 3rd side, added its val and encrypted it {} to 1st side'.format(res))

    res = rsa_generation.encrypt(s3_public, rsa_generation.decrypt(s1_private, res) + s1_val)
    print('1st side decrypted val from 2nd side, added its val and encrypted it {} to 3rd side'.format(res))

    res = (rsa_generation.decrypt(s3_private, res) - x) / 3
    print('Avg value is ' + str(res))
    return res

# ========= secret storing by means of gamma ==========

def gamma_store_secret(secret:int, g1:int, g2:int, g3:int):
    print('1st side has gamma {}'.format(g1))
    print('2nd side has gamma {}'.format(g2))
    print('3rd side has gamma {}'.format(g3))

    cipher = secret ^ g1 ^ g2 ^ g3 
    print('Cipher for the secret is {}'.format(cipher))

    print('Secret is {}'.format(cipher ^ g1 ^ g2 ^ g3))


# ======== secret separation by Shamir ==============
def shamir_separete_secret_3_5(secret:int):
    p = randint(secret if secret > 5 else 5, 1000)
    print('simple num p is {}'.format(p))
    a2 = randint(0, 1000)
    a1 = randint(0, 1000)
    print('koefs a1 ({}) and a2 ({})'.format(a1, a2))
    f = lambda x: (a2*x**2 + a1*x + secret) % p

    x = -2
    parts = [ (x+i, f(x+i)) for i in range(5) ]
    print('Calculated parts: ' + str(parts))


# ========== secret separetion by Asmut-BLum ==============
def asmut_blum_separete_secret(secret:int):
    p = 4
    while not rsa_generation.is_prime(p):
        p = randint(secret, 100)
    print('Simple num p is {}'.format(p))
    
    d = [0,0,0,0,0]
    d[0] = p+1

    for i in range(1,5):
        d[i] = d[i-1]+1
        is_simple = False
        while not is_simple:
            is_simple = True
            for j in range(0,i):
                if rsa_generation.gcd(d[i], d[j]) != 1:
                    is_simple = False
                    break;
            if not is_simple:
                d[i] += 1
    print('Simple d\'s :' + str(d))

    prod = 1
    for el in d:
        prod *= el
    r = randint(0, (prod - secret) // p)
    print('r is {}'.format(r))
    
    secret2 = secret + r * p
    print('S\' is {}'.format(secret2))

    parts = [ (d[i], secret2 % d[i]) for i in range(5) ]
    print('Calculated parts: ' + str(parts))




if __name__ == '__main__':
    rsa_calc_avg(50, 100, 30)
    gamma_store_secret(15, 10, 20, 22)
    shamir_separete_secret_3_5(20)
    asmut_blum_separete_secret(20)
