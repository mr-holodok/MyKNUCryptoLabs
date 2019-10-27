# ==================================
# #1 Simple Single Permutations Cipher
# ==================================

import random

def GenerateCiphershiftTable(length: int) -> list:
    table = list(length * '0')
    for i in range(0, length):
        hit = False
        while not hit:
            num = random.randint(1, length)
            if table[num - 1] == '0':
              hit = True
        table[num - 1] = i + 1
    return table 

def EncodeSimpleSinglePermutation(msg:str, cipherTable: list) -> str:
    encoded = list(msg)
    for i in range(0, len(msg)):
        encoded[i] = msg[cipherTable[i] - 1]
    encodedStr = str()
    for i in range(0, len(msg)):
        encodedStr += encoded[i]
    return encodedStr 


# ==================================
# #2 Block Single Permutations Cipher
# ==================================

def EncodeBlockSinglePermutation(msg:str, cipherTable: list) -> str: 
    mod = len(msg) % len(cipherTable)
    if mod != 0:
        msg += (len(cipherTable) - mod) * '*'
    encoded = list(msg)
    for i in range(0, len(encoded)):
        encoded[i] = msg[len(cipherTable) * (i // len(cipherTable)) + cipherTable[i % len(cipherTable)] - 1]
    encodedStr = str()
    for i in range(0, len(encoded)):
        encodedStr += encoded[i]
    return encodedStr 


# ==================================
# #3 Table Route Permutation Cipher 
# ==================================

def PrintTableRoutePermutationTable(msg: str, tableWidth: int):
    mod = len(msg) % tableWidth 
    if mod != 0:
        msg += (tableWidth - mod) * '*'
    for i in range(0, len(msg) // tableWidth):
        print(msg[0+tableWidth*i:tableWidth+tableWidth*i])

def EncodeTableRoutePermutation(msg: str, tableWidth: int) -> str:
    mod = len(msg) % tableWidth 
    if mod != 0:
        msg += (tableWidth - mod) * '*'
    encoded = list(msg)
    ind = 0 
    for i in range(0, tableWidth):
        for j in range(0, len(encoded) // tableWidth):
            encoded[ind] = msg[i + j * tableWidth]
            ind += 1
    encodedStr = str()
    for i in range(0, len(encoded)):
        encodedStr += encoded[i]
    return encodedStr 

# ==================================
# #4 Vertical Permutation Cipher
# ==================================

def PrintVertiacalPermutationCipherTable(msg:str, key: str):
    mod = len(msg) % len(key)
    if mod != 0:
        msg += (len(key) - mod) * '*'
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  
    key = key.upper()
    keyIndexTable = list(key)
    index = 1
    for ch in alphabet:
        while ch in keyIndexTable:
            keyIndexTable[keyIndexTable.index(ch)] = index
            index += 1
    for i in range(0, len(key)):
        print(key[i], end='\t')
    print()
    for i in range(0, len(key)):
        print(keyIndexTable[i], end='\t')
    print()
    for i in range(0, len(msg) // len(key)):
        for ch in msg[0+len(key)*i:len(key)+len(key)*i]:
            print(ch, end='\t')
        print()

def EncodeVerticalPermutation(msg: str, key: str) -> str:
    mod = len(msg) % len(key)
    if mod != 0:
        msg += (len(key) - mod) * '*'
    encoded = list(msg)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    keyIndexTable = list(key)
    index = 1
    for ch in alphabet:
        while ch in keyIndexTable:
            keyIndexTable[keyIndexTable.index(ch)] = index
            index += 1
    index = 0
    for j in range(0, len(encoded) // len(key)):
        for i in keyIndexTable:
            encoded[j * len(key) + i - 1] = msg[index]
            index += 1
    encodedStr = str()
    for i in range(0, len(encoded)):
        encodedStr += encoded[i]
    return encodedStr 

# ==================================
# #5 Rotation Cross Cipher
# ==================================

def PrintRotationCrossTables(msg: str):
    mod = len(msg) % 16
    if mod != 0:
        msg += (16 - mod) * '*'
    encoded = list(len(msg) * ' ')
    masks = list()
    masks.append([0, 2, 9, 11])
    masks.append([1, 3, 8, 10])
    masks.append([4, 6, 13, 15])
    masks.append([5, 7, 12, 14])
    msgInd = 0
    for tableInd in range(0, len(msg) // 16):
        for maskIndexes in masks:
            for maskIndex in maskIndexes:
                encoded[tableInd * 16 + maskIndex] = msg[msgInd]
                msgInd += 1
            for i in range(0 + tableInd * 16, 16 + tableInd * 16):
                if i % 4 == 0:
                    print()
                print(encoded[i], end='\t')  
            print()

def EncodeRotationCross(msg:str) -> str:
    mod = len(msg) % 16
    if mod != 0:
        msg += (16 - mod) * '*'
    encoded = list(msg)
    masks = list()
    masks.append([0, 2, 9, 11])
    masks.append([1, 3, 8, 10])
    masks.append([4, 6, 13, 15])
    masks.append([5, 7, 12, 14])
    msgInd = 0
    for tableInd in range(0, len(msg) // 16):
        for maskIndexes in masks:
            for maskIndex in maskIndexes:
                encoded[tableInd * 16 + maskIndex] = msg[msgInd]
                msgInd += 1
    encodedStr = str()
    for i in range(0, len(encoded)):
        encodedStr += encoded[i]
    return encodedStr 

# ==================================
# #6 Magic Square
# ==================================

def PrintMagicSquare():
    sqr = [[16,3,2,13], [5,10,11,8], [9,6,7,12], [4,15,14,1]]
    for i in range(0, len(sqr)):
        for num in sqr[i]:
            print(num, end='\t')
        print()

def PrintMagicSquareTables(msg: str):
    mod = len(msg) % 16
    if mod != 0:
        msg += (16 - mod) * '*'
    encoded = list(msg)
    sqr = [[16,3,2,13], [5,10,11,8], [9,6,7,12], [4,15,14,1]]
    encodeIndex = 0
    for tableInd in range(0, len(msg) // 16):
        for row in sqr:
            for index in row:
                encoded[encodeIndex] = msg[tableInd * 16 + index - 1]
                encodeIndex += 1
        for i in range(0 + tableInd * 16, 16 + tableInd * 16):
            if i % 4 == 0:
                print()
            print(encoded[i], end='\t')  
        print()


def EncodeMagicSquare(msg: str) -> str:
    mod = len(msg) % 16
    if mod != 0:
        msg += (16 - mod) * '*'
    encoded = list(msg)
    sqr = [[16,3,2,13], [5,10,11,8], [9,6,7,12], [4,15,14,1]]
    encodeIndex = 0
    for tableInd in range(0, len(msg) // 16):
        for row in sqr:
            for index in row:
                encoded[encodeIndex] = msg[tableInd * 16 + index - 1]
                encodeIndex += 1
    encodedStr = str()
    for i in range(0, len(encoded)):
        encodedStr += encoded[i]
    return encodedStr 

# ==================================
# #7 Double Permutation
# ==================================

columns = [2,3,6,1,5,4]

def PrintColumnShift():
    print([x for x in range(1, len(columns)+1)])
    print(columns)

rows = [4,1,3,2]

def PrintRowShift():
    print([x for x in range(1, len(rows)+1)])
    print(rows)

def PrintDoublePermutationTables(msg:str):
    mod = len(msg) % (len(rows)*len(columns))
    if mod != 0:
        msg += (len(rows)*len(columns) - mod) * '*'
    encoded = list(msg)
    encodedTwice = list(msg)
    encodeIndex = 0
    encodeTwiceIndex = 0
    for tableInd in range(0, len(msg) // (len(rows)*len(columns))):
        for i in range(0, len(rows)):
            for index in columns:
                encoded[encodeIndex] = msg[tableInd * len(rows) * len(columns) + i * len(columns) + index - 1]
                encodeIndex += 1
        for i in range(0 + tableInd * len(rows) * len(columns), len(rows) * len(columns) + tableInd * len(rows) * len(columns)):
            if i % len(columns) == 0:
                print()
            print(encoded[i], end='\t')
        print()
        for i in rows:
            for index in range(0, len(columns)):
                encodedTwice[encodeTwiceIndex] = encoded[tableInd * len(rows) * len(columns) + (i - 1) * len(columns) + index]
                encodeTwiceIndex += 1
        for i in range(0 + tableInd * len(rows) * len(columns), len(rows) * len(columns) + tableInd * len(rows) * len(columns)):
            if i % len(columns) == 0:
                print()
            print(encodedTwice[i], end='\t') 
        print()


def EncodeDoublePermutation(msg:str) -> str:
    mod = len(msg) % (len(rows)*len(columns))
    if mod != 0:
        msg += (len(rows)*len(columns) - mod) * '*'
    encoded = list(msg)
    encodedTwice = list(msg)
    encodeIndex = 0
    encodeTwiceIndex = 0
    for tableInd in range(0, len(msg) // (len(rows)*len(columns))):
        for i in range(0, len(rows)):
            for index in columns:
                encoded[encodeIndex] = msg[tableInd * len(rows) * len(columns) + i * len(columns) + index - 1]
                encodeIndex += 1
        for i in rows:
            for index in range(0, len(columns)):
                encodedTwice[encodeTwiceIndex] = encoded[tableInd * len(rows) * len(columns) + (i - 1) * len(columns) + index]
                encodeTwiceIndex += 1
    encodedStr = str()
    for i in range(0, len(encodedTwice)):
        encodedStr += encodedTwice[i]
    return encodedStr 



if __name__ == "__main__":
    
    #print('Simple Single Permutations Cipher')
    #print('Please, enter the message:')
    #msg = input()
    #table = GenerateCiphershiftTable(len(msg))
    #print('Cipher table looks like:')
    #print(str(table))
    #print('Your encoded message looks like:')
    #print(EncodeSimpleSinglePermutation(msg, table))

    #print('Block Single Permutations Cipher')
    #print('Please, enter the message:')
    #msg = input()
    #table = GenerateCiphershiftTable(4)
    #print('Cipher table looks like:')
    #print(str(table))
    #print('Your encoded message looks like:')
    #print(EncodeBlockSinglePermutation(msg, table))

    #print('Table Route Permutation Cipher ')
    #print('Please, enter the message:')
    #msg = input()
    #print('Cipher table looks like:')
    #PrintTableRoutePermutationTable(msg, 4)
    #print('Your encoded message looks like:')
    #print(EncodeTableRoutePermutation(msg, 4))
    
    #print('Vertical Permutation Cipher ')
    #print('Please, enter the message:')
    #msg = input()
    #print('Please, enter the key:')
    #key = input()
    #print('Cipher table looks like:')
    #PrintVertiacalPermutationCipherTable(msg, key)
    #print('Your encoded message looks like:')
    #print(EncodeVerticalPermutation(msg, key))

    #print('Rotation Cross Cipher')
    #print('Please, enter the message:')
    #msg = input()
    #print('Cipher table looks like:')
    #PrintRotationCrossTables(msg)
    #print('Your encoded message looks like:')
    #print(EncodeRotationCross(msg))

    #print('Magic Square')
    #print('Please, enter the message:')
    #msg = input()
    #print('Magic Square looks like:')
    #PrintMagicSquare()
    #print('Cipher table looks like:')
    #PrintMagicSquareTables(msg)
    #print('Your encoded message looks like:')
    #print(EncodeMagicSquare(msg))

    print('Double Permutation')
    print('Please, enter the message:')
    msg = input()
    print('Column Permutation Table looks like:')
    PrintColumnShift()
    print('Row Permutation Table looks like:')
    PrintRowShift()
    print('Cipher table looks like:')
    PrintDoublePermutationTables(msg)
    print('Your encoded message looks like:')
    print(EncodeDoublePermutation(msg))