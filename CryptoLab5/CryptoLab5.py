import random

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

# -------------------------
# RSA
# -------------------------

# p = 11 , q = 23
rsa_n = 253
# Euler function F(n) = (p - 1)*(q - 1) = 220
rsa_e = 17
# e * d mod F(n) = 1, d = 13
rsa_d = 13

def encryptRSA(msg: str, n: int, e: int) -> str:
    msg = list(msg.upper())
    encod = list()
    for char in msg:
        encod.append(alphabet.index(char) ** e % n)
    return ' '.join(map(str, encod))

def decryptRSA(encod: str, n: int, d: int) -> str:
    msg = list()
    encod = list(map(int, encod.split()))
    for num in encod:
        msg.append(alphabet[ num ** d % n ])
    return ''.join(msg)

# -------------------------
# Knapsack 
# ------------------------- 

knapsack_private_key = list([2, 3, 6, 13, 27, 52, 105, 210])
knapsack_open_key = list([62, 93, 186, 403, 417, 352, 315, 210])

def GetKnapsackValue(char:str, key:list) -> int:
    code = int.from_bytes(char.encode('cp1251'), 'little') # get code for ukr encoding
    value = 0
    for i in range(0, len(key)):
        if code & (1 << i) == 1 << i:
            value += key[len(key) - i - 1]
    return value

def EncodeKnapsack(msg: str, key:list) -> str:
    encoded = list()
    for char in msg:
        encoded.append(GetKnapsackValue(char, key))
    return ' '.join(map(str, encoded))

# -------------------------
# El Gamal
# ------------------------- 

el_p = 37
el_g = 2
el_x = 5
el_y = el_g ** el_x % el_p

def EncodeElGamal(msg:str, g:int, p:int, y:int):
    part1, part2 = list(), list()
    for char in msg:
        k = random.randint(2, p-2)
        part1.append( (g ** k) % p)
        part2.append( ((y ** k) * alphabet.index(char.upper())) % p)
    return part1, part2

def DecodeElGamal(part1:list, part2:list, p:int, privateKey:int):
    result = list()
    for i in range(0, len(part1)):
        result.append(alphabet[part2[i] * part1[i] ** (p - 1 - privateKey) % p])
    return ''.join(result)


if __name__ == "__main__": 
    print("RSA")
    print("Please print message that you want to encode:")
    msg = input()
    print("Open key pair: (%d, %d)" %(rsa_n, rsa_e))
    print("Private key pair: (%d, %d)" %(rsa_n, rsa_d))
    print("Encrypted message: " + encryptRSA(msg, rsa_n, rsa_e))
    
    print()
    print('Knapsack')
    print("Please print message that you want to encode:")
    msg = input()
    print("Open key: " + ' '.join(map(str, knapsack_open_key)))
    print("Private key: " + ' '.join(map(str, knapsack_private_key)))
    print("Encrypted message: " + EncodeKnapsack(msg, knapsack_open_key))

    print()
    print('El Gamal')
    print("Please print message that you want to encode:")
    msg = input()
    print("Open key: " + ' '.join(map(str, [el_p, el_g, el_y])))
    print("Private key: " + str(el_x))
    a, b = EncodeElGamal(msg, el_g, el_p, el_y)
    print("Encrypted message: ")
    print("a: " + ' '.join(map(str, a)))
    print("b: " + ' '.join(map(str, b)))