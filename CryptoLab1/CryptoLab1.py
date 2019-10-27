import math
import random

# =================
# Caesar cipher
# =================

def CaesarCiferEncrypt(message: str, shift: int) -> str:
    if shift < 1:
        raise Exception("Shift must be greater than 0!")
    encryptedText = str()
    for char in message:
        encryptedText += chr(ord(char) + shift)
    return encryptedText

# =================
# Slogan cipher
# =================

def SloganTableGenerator(slogan: str) -> str:
    table = str()
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    for char in slogan.upper() + alphabet:
        if char not in table:
            table += char
    if len(table) < 36:
        table += (36 - len(table)) * ' '
    return table

def SloganCipher(sloganTable: str, message: str) -> str:
    # valid only for English messages
    message = message.upper()
    encryptedText = str()
    spaceIndex = sloganTable.index(' ')
    for char in message:
        if char == ' ':
            encryptedText += sloganTable[spaceIndex]
        else:
            encryptedText += sloganTable[ord(char) - 65]
    return encryptedText

# =================
# Polibius square
# =================

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
squareWidth = 6

def PolibiusSquareCipher(message: str) -> str:
    # valid only for English messages
    encryptedText = str()
    for char in message.upper():
        charIndex = alphabet.index(char) + 1
        row = math.ceil(charIndex / squareWidth)
        column = charIndex % squareWidth
        if column == 0:
            column = squareWidth
        encryptedText += str(row) + str(column) + ' '
    return encryptedText

def PrintPolibiusSquare(alphabet: str):
    col = 1
    for char in alphabet:
        print(char, end='\t')
        col += 1
        if col > 6:
            print()
            col = 1
    print()

# =================
# Trisemus System
# =================

def TrisemusCipher(table: str, message: str) -> str:
    # valid only for English messages
    encryptedText = str()
    for char in message.upper():
        charIndex = table.index(char) + 1
        row = math.ceil(charIndex / squareWidth) + 1
        if row > 5:
            row = 1
        column = charIndex % squareWidth
        if column == 0:
            column = squareWidth
        if row == 5 and column > 3:
            column = 1
        encryptedText += table[(row - 1) * squareWidth + column - 1]
    return encryptedText

# =================
# Playfair Cipher
# =================

def PlayfairCipher(table: str, message: str) -> str:
    encryptedText = str()
    switchChar = 'X'
    bigramText = str()
    message = message.upper()

    i = 0
    while i < len(message):
        if i + 1 < len(message):
            bigram = message[i:i+2]
            if bigram[0] == bigram[1]:
                bigram = bigram[0] + switchChar
                i -= 1
            i += 2
            bigramText += bigram
        else:
            message += switchChar

    i = 0
    while i < len(bigramText):
        
        bi1Index = table.index(bigramText[i]) + 1
        bi1Row = math.ceil(bi1Index / squareWidth)
        bi1Col = bi1Index % squareWidth
        if bi1Col == 0:
            bi1Col = squareWidth

        bi2Index = table.index(bigramText[i+1]) + 1
        bi2Row = math.ceil(bi2Index / squareWidth)
        bi2Col = bi2Index % squareWidth
        if bi2Col == 0:
            bi2Col = squareWidth

        if bi1Row == bi2Row:
            bi1Right = bi1Col % squareWidth + 1
            if bi1Row == 5 and bi1Right > 3:
                bi1Right = 1
            bi2Right = bi2Col % squareWidth + 1
            if bi2Row == 5 and bi2Right > 3:
                bi2Right = 1
            encryptedText += table[(bi1Row - 1) * squareWidth + bi1Right - 1] + \
                            table[(bi1Row - 1) * squareWidth + bi2Right - 1] + ' '
        elif bi1Col == bi2Col:
            bi1Bottom = bi1Row % 5 + 1
            bi2Bottom = bi2Row % 5 + 1
            encryptedText += table[(bi1Bottom - 1) * squareWidth + bi1Col - 1] + \
                            table[(bi2Bottom - 1) * squareWidth + bi1Col - 1] + ' '
        else:
            encryptedText += table[(bi1Row - 1) * squareWidth + bi2Col - 1] + \
                            table[(bi2Row - 1) * squareWidth + bi1Col - 1] + ' '
        
        i += 2
        

    return encryptedText

# =================
# Homophonic Cipher
# =================

freq1 = [805, 161, 261, 392, 1222, 214, 253, 557, 709, 10, 94, 419, 258, 682, 761, 194, 11, 590, 644, 928, 285, 101, 219, 18, 205, 7]
freq2 = [828, 149, 278, 425, 1270, 222, 201, 609, 696, 15, 77, 402, 240, 674, 750, 192,  9, 598, 632, 905, 275,  97, 236, 15, 197, 8]

def HomophonicCipher(message: str) -> str:
    message = message.replace(' ', '').upper()
    encryptedText = str()
    usedLetters1 = str()
    usedLetters2 = str()

    for char in message:
        if char in usedLetters1:
            usedLetters2 += char
            encryptedText += str(freq2[ord(char) - 65]) + ' '
        elif char in usedLetters2:
            if random.randint(0, 1) == 0:
                encryptedText += str(freq1[ord(char) - 65]) + ' '
            else:
                encryptedText += str(freq2[ord(char) - 65]) + ' '
        else:
            usedLetters1 += char
            encryptedText += str(freq1[ord(char) - 65]) + ' '
    return encryptedText

# =================
# Vigenere Cipher
# =================

def VigenereCipher(key: str, message: str) -> str:
    longKey = key
    while len(longKey) < len(message):
        longKey += key

    encryptedText = str()
    message = message.replace(' ', '').upper()
    longKey = longKey.replace(' ', '').upper()
    for i in range(0, len(message)):
        col = alphabet.index(message[i])
        row = alphabet.index(longKey[i])
        shiftedAlphabet = alphabet[row:-1] + alphabet[0:row]
        encryptedText += shiftedAlphabet[col]
    return encryptedText


if __name__ == "__main__":
    print("Please, enter the shift of Caesar cipher (positive integer): ", end='')
    shift = int(input())
    print("Please, enter text that you want to encode:")
    message = input()
    print("Your encoded message look like: \n" + CaesarCiferEncrypt(message, shift))

    print("Please, enter the slogan for Slogan Cipher: ", end='')
    slogan = input()
    table = SloganTableGenerator(slogan)
    print("Table for your slogan:" + table)
    print("Please, enter text that you want to encode:")
    message = input()
    print("Your encoded message look like: \n" + SloganCipher(table, message))

    print("Please, enter text that you want to encode with Polibius square:")
    message = input()
    PrintPolibiusSquare(alphabet)
    print("Your encoded message look like: \n" + PolibiusSquareCipher(message))

    print("Please, enter the slogan for the Table of the Trisemus system: ", end='')
    slogan = input()
    table = SloganTableGenerator(slogan)
    print("Table for your slogan:" + table)
    print("Please, enter text that you want to encode with Trisemus system:")
    message = input()
    PrintPolibiusSquare(table)
    print("Your encoded message look like: \n" + TrisemusCipher(table, message))

    print("Please, enter the slogan for the Table of the Playfair cipher: ", end='')
    slogan = input()
    table = SloganTableGenerator(slogan)
    print("Table for your slogan:")
    PrintPolibiusSquare(table)
    print("Please, enter text that you want to encode with Playfair cipher:")
    message = input()
    print("Your encoded message look like: \n" + PlayfairCipher(table, message))

    print("Homophonic freq tables:")
    print(freq1)
    print(freq2)
    print("Please, enter text that you want to encode with Homophonic cipher:")
    message = input()
    print("Your encoded message look like: \n" + HomophonicCipher(message))

    print("Please, enter the key for the Table of the Vigenere cipher: ", end='')
    key = input()
    print("Please, enter text that you want to encode with Vigenere cipher:")
    message = input()
    print("Your encoded message look like: \n" + VigenereCipher(key, message))