import numpy as np


# calculates parity bit
def calc_parity(data:int, even_parity=True) -> int:
    count = 0
    # check every bit (bin(data) returns additional 0b)
    for i in range(len(bin(data))-2):
        # check if bit is 1
        if (data & 2**i) == 2**i:
            count += 1
    if even_parity:
        return 1 if count % 2 != 0 else 0
    else:
        return 0 if count % 2 != 0 else 1

def calc_parity_for_cp1251(data: str):
    for ch in data:
        code = int.from_bytes(ch.encode('cp1251'), 'little')
        print(ch + '\t' + bin(code) + '\teven parity: ' + str(calc_parity(code)) + \
            '\todd parity: ' + str(calc_parity(code, even_parity=False)))


def lun_algo(data:str):
    if len(data) % 2 == 0:
        prepared = [int(i) for i in list(data)]
        even_sum = 0
        for i in range(len(prepared))[0::2]:
            prepared[i] = (int(prepared[i]) * 2) % 9
            even_sum += prepared[i]
        odd_sum = sum(prepared[1:-1:2])
        return 10 - ((even_sum + odd_sum) % 10)
    else:
        prepared = [int(i) for i in list(data)]
        odd_sum = 0
        for i in range(len(prepared))[1::2]:
            prepared[i] = (int(prepared[i]) * 2) % 9
            odd_sum += prepared[i]
        even_sum = sum(prepared[0:-1:2])
        return 10 - ((even_sum + odd_sum) % 10)


def get_control_cipher_EAN_13(data: str):
    nums = [int(i) for i in list(data)]
    odd_sum = sum(nums[0:-1:2])
    even_sum = 3*sum(nums[1::2])
    return 10 - ((even_sum + odd_sum) % 10)


def get_control_cipher_for_taxpayer_id(data: str):
    n = [int(i) for i in list(data)]
    return ((2*n[1] + 4*n[2] + 10*n[3] + 3*n[4] + 5*n[5] + 9*n[6] + 4*n[7] + 6*n[8] + 8*n[9]) % 11 ) % 10 


def get_control_cipher_for_railway_station(data: str):
    n = [int(i) for i in list(data)]
    cipher = (n[1] + 2*n[2] + 3*n[3] + 4*n[4] + 5*n[5]) % 11
    if cipher < 10:
        return cipher
    else: 
        cipher = (3*n[1] + 4*n[2] + 5*n[3] + 6*n[4] + 7*n[5]) % 11
        if cipher < 10:
           return cipher
        else:
           return 0


def calc_CRC_4_ITU(data: int) -> int:
    bits = [int(i) for i in list(bin(data)[2:])]
    bits.extend([0,0,0,0])
    poly = [1,0,0,1,1]

    curr = bits[0:5]
    for iter in range(5):
        if curr[0] == 1:
            curr = bin_list_xor(curr, poly)
        # shifting
        curr = curr[1:]
        if 5 + iter < len(bits):
            curr.append(bits[5+iter])

    s = "".join(map(str, curr))
    #print("".join(map(str, curr)))
    return int("".join(map(str, curr)), 2)


def bin_list_xor(l1:list, l2:list) -> list:
    # len is equal
    res = list()
    for i in range(len(l1)):
        res.append(l1[i] ^ l2[i])
    return res


def calc_error_correcting_code(bin_data:str, control_bits:str, parity_bit:str) -> tuple:
    b = [int(i) for i in bin_data]
    c = [int(i) for i in control_bits]
    xr = list()
    xr.extend(c[0:2])
    xr.append(b[0])
    xr.append(c[2])
    xr.extend(b[1:4])
    xr.append(c[3])
    xr.extend(b[4:])

    parity = calc_parity(int("".join(map(str,xr)), 2))
       
    n = list()
    for i in range(1,16):
        n.append([int(i) for i in "{0:#0{1}b}".format(i, 6)[2:]])

    xr = np.array(xr)
    nt = np.array(n)
    s = [ i % 2 for i in np.matmul(xr, nt)]

    return tuple([s,parity])

def analyze_ecc_results(bin_data:str, control_bits:str, parity_bit:str):
    s, p = calc_error_correcting_code(bin_data, control_bits, parity_bit)
    if p != int(parity_bit):
        print('Parity bits are different!')
    else:
        print('Parity bits are equal!')

    print('There are ' + str(s.count(1)) + ' 1\'s in the syndrome vector')
    print(s)

def calc_error_correcting_code_control_bits(bin_data:str) -> tuple:
    b = [int(i) for i in bin_data]
    xr = list()
    xr.extend([0,0])
    xr.append(b[0])
    xr.append(0)
    xr.extend(b[1:4])
    xr.append(0)
    xr.extend(b[4:])

    parity = calc_parity(int("".join(map(str, xr)), 2))
       
    n = list()
    for i in range(1,16):
        n.append([int(i) for i in "{0:#0{1}b}".format(i, 6)[2:]])

    r = list()
    for j in range(4):
        sum = 0
        for i in range(len(xr)):
            sum += (xr[i] * n[i][j])
        sum %= 2
        r.append(sum)

    return tuple([r,parity])



if __name__ == '__main__':
    #print('======= Checking parity =========')
    #print('Please, enter the data: ', end='')
    #data = input()
    #calc_parity_for_cp1251(data)
    
    #print('======== Lun algoithm =========')
    #print('Please, enter the number(15 ciphers): ', end='')
    #num = input()
    #print('Control cipher should be: ' + str(lun_algo(num)))

    #print('======== EAN-13 standart =========')
    #print('Please, enter the number(13 ciphers): ', end='')
    #num = input()
    #print('Control cipher should be: ' + str(get_control_cipher_EAN_13(num)))

    #print('======== Taxpayer ID =========')
    #print('Please, enter the number(10 ciphers): ', end='')
    #num = input()
    #print('Control cipher should be: ' + str(get_control_cipher_for_taxpayer_id(num)))

    #print('======== Railway station =========')
    #print('Please, enter the number(6 ciphers): ', end='')
    #num = input()
    #print('Control cipher should be: ' + str(get_control_cipher_for_railway_station(num)))

    #print('======== CRC-4-ITU =========')
    #print('Please, enter the number (up to 32): ', end='')
    #num = int(input())
    #print('Control sum is: ' + str(calc_CRC_4_ITU(num)))

    print('======== ECC =========')
    print('Please, enter the info bits, control bits and parity bit (separated by space): ')
    data = input()
    data = data.split()
    real =  calc_error_correcting_code_control_bits(data[0])
    print('real control bits and parity bit: ' + str(real[0]) + ' ' + str(real[1]))


    analyze_ecc_results(data[0], data[1], data[2])