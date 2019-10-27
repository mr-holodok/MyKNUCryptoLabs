alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

def GetCharIndex(ch: str) -> int:
    return alphabet.index(ch.upper())

def GetCharAtIndex(index: int) -> str:
    return alphabet[index]

def EncodeGammaN(msg:str, gamma:str):
    count = len(msg) // len(gamma)
    if len(msg) > len(gamma):
        gamma += gamma * count 
    encoded = str()
    for i in range(0, len(msg)):
        encoded += GetCharAtIndex((GetCharIndex(msg[i]) + GetCharIndex(gamma[i])) % len(alphabet))
    return encoded

def EncodeGamma2(msg:str, gamma:str):
    count = len(msg) // len(gamma)
    if len(msg) > len(gamma):
        gamma += gamma * count 
    encoded = str()
    for i in range(0, len(msg)):
        encoded += GetCharAtIndex((GetCharIndex(msg[i]) ^ GetCharIndex(gamma[i])) % len(alphabet))
    return encoded

def PrintGammaIndexes(msg:str, gamma:str, cipher: str):
    count = len(msg) // len(gamma)
    if len(msg) > len(gamma):
        gamma += gamma * count 

    for i in range(0, len(msg)):
        print(gamma[i], end='\t')
    print()
    for i in range(0, len(msg)):
        print(GetCharIndex(gamma[i]), end='\t')
    print('\n')

    for i in range(0, len(msg)):
        print(msg[i], end='\t')
    print()
    for i in range(0, len(msg)):
        print(GetCharIndex(msg[i]), end='\t')
    print('\n')

    for i in range(0, len(msg)):
        print(cipher[i], end='\t')
    print()
    for i in range(0, len(msg)):
        print(GetCharIndex(cipher[i]), end='\t')
    print()

if __name__ == "__main__":
    print("Gamma shift modulo N:")
    print("Please, enter the message that you want to encode:")
    message = input()
    print("Please, enter the gamma: ")
    gamma = input()
    cipher = EncodeGammaN(message, gamma)
    print("Your encoded message look like: \n" + cipher)
    PrintGammaIndexes(message, gamma, cipher)

    print("Gamma shift modulo 2:")
    print("Please, enter the message that you want to encode:")
    message = input()
    print("Please, enter the gamma: ")
    gamma = input()
    cipher =  EncodeGamma2(message, gamma)
    print("Your encoded message look like: \n" + cipher)
    PrintGammaIndexes(message, gamma, cipher)
