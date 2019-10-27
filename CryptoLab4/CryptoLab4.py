import math

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
squareWidth = 6

def EncodeADFGVX(message: str, key: str) -> str:
    # valid only for English messages
    encryptedText = str()
    colNames = 'ADFGVX' # row and column names
    for char in message.upper():
        charIndex = alphabet.index(char)
        row = charIndex // squareWidth
        column = charIndex % squareWidth
        encryptedText += colNames[row] + colNames[column]

    tableRank = list(key.upper()) 
    # list that contains indexes of chars in key sorted by alphabet and this list is the route for writing out

    index = 0
    for ch in alphabet:
        while ch in tableRank:
            tableRank[tableRank.index(ch)] = index
            index += 1

    encoded = list()
    for i in range(0, len(tableRank)):
        index = tableRank.index(i)
        while index < len(encryptedText):
            encoded.append(encryptedText[index])
            index += len(key)
    return ''.join(encoded) 
  

def PrintKeyAndRanks(key: str):
    for char in key:
        print(char, end='\t')
    print()

    index = 0
    tableRank = list(key.upper()) 
    for ch in alphabet:
        while ch in tableRank:
            tableRank[tableRank.index(ch)] = index
            index += 1
    for ind in tableRank:
        print(ind, end='\t')
    print()

def PrintADFGVXTableFromStage1():
    for char in '\|ADFGVX':
        print(char, end='\t')
    print()
    for char in '\|ADFGVX':
        print('-', end='\t')
    print()
    col = 1
    rows = 'ADFGVX'
    rowInd = 0
    # TODO: looks ugly and print(X) at the end (strange)
    print(rows[rowInd] + '\t|', end='\t')
    for char in alphabet:
        print(char, end='\t')
        col += 1
        if col > 6:
            print()
            col = 1
            rowInd += 1 
            print(rows[rowInd] + '\t|', end='\t')
    print()
    print('X\t|')
    print()

def PrintADFGVXTableFromStage2(message: str, key: str):
    encryptedText = str()
    colNames = 'ADFGVX' # row and column names
    for char in message.upper():
        charIndex = alphabet.index(char)
        row = charIndex // squareWidth
        column = charIndex % squareWidth
        encryptedText += colNames[row] + colNames[column]
    print('Encrypted text from first stage:')
    print(''.join(encryptedText))
    PrintKeyAndRanks(key)
    index = 0
    while index < len(encryptedText):
        print(encryptedText[index], end='\t')
        index += 1
        if index % len(key) == 0:
            print()
    print()


if __name__ == "__main__":
    print("ADFGVX cipher")
    print("Please, enter the key needed for encoding:")
    key = input()
    print("Please, enter the text that you want to encode:")
    message = input()
    PrintADFGVXTableFromStage1()
    PrintADFGVXTableFromStage2(message, key)
    result = EncodeADFGVX(message, key) 
    print("Your encoded message look like: \n" + ' '.join(result[i:i+5] for i in range(0,len(result),5)))  
