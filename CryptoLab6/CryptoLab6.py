def RepresentAsSignMagnitude(code: str, dataLen: int) -> str:
    sign = True if code[0] == '-' else False
    num = abs(int(code))
    bin = '1' if sign else '0'
    binAbsNum = '{0:b}'.format(num)
    bin += '0' * (dataLen - 1 - len(binAbsNum)) + binAbsNum 
    return bin

def InvertBinStr(binCode: str) -> str:
    binCode = list(binCode)
    for i in range(0, len(binCode)):
        if binCode[i] == '1':
            binCode[i]  = '0'
        elif binCode[i]  == '0':
            binCode[i]  = '1'
    return ''.join(binCode)

def RepresentAsFirstComplement(code: str, dataLen: int) -> str:
    sign = True if code[0] == '-' else False
    num = abs(int(code))
    bin = '1' if sign else '0'
    binAbsNum = '{0:b}'.format(num)
    binAbsNumShifted = '0' * (dataLen - 1 - len(binAbsNum)) + binAbsNum 
    bin += InvertBinStr(binAbsNumShifted) if sign else binAbsNumShifted
    return bin

def RepresentAsSecondComplement(code: str, dataLen: int) -> str:
    sign = True if code[0] == '-' else False
    num = abs(int(code))
    binAbsNum = '{0:b}'.format(num)
    if len(binAbsNum) > dataLen - 1:
        binAbsNum = binAbsNum[-dataLen+1:]
    binAbsNumShifted = '0' * (dataLen - 1 - len(binAbsNum)) + binAbsNum 
    if sign:
        # add 1 to bin number
        carry = 1
        binList = list(InvertBinStr(binAbsNumShifted))
        for i in range(len(binList)-1, -1, -1):
            if int(binList[i]) + carry == 1:
                binList[i] = '1'
                break
            else:
                binList[i] = '0'
        return '1' + ''.join(binList)
    else:
        return '0' + binAbsNumShifted

def DecFractionToBinFraction(frac: float, FracResultLen: int) -> str:
    binRepr = list()
    step = 0
    while step < FracResultLen:
        frac = frac * 2
        if frac >= 1:
            frac -= 1
            binRepr.append('1')
        elif frac == 0:
            while step < FracResultLen:
                binRepr.append('0')
                step += 1
        else:
            binRepr.append('0')
        step += 1
    return ''.join(binRepr)

def RepresentAsFloatingWithSignForMantissAndSignForExponent(code: float):
    exponent = 0
    sign = True if code < 0 else False
    code = abs(code)
    if code > 1:
        for i in range(1, 128):
            if 2 ** i > code:
                exponent = i-1
                break
    else:
        for i in range(1, 127):
            if 2 ** -i <= code:
                exponent = -i
                break
    remainder = code / 2 ** exponent
    if remainder >= 1:
        remainder -= 1
    mantiss = DecFractionToBinFraction(remainder, 15)
    return ('0 ' if exponent >= 0 else '1 ') + '0' * (7 - len('{0:b}'.format(abs(exponent)))) + '{0:b}'.format(abs(exponent)) + (' 1 ' if sign else ' 0 ') + ''.join(mantiss)

def RepresentAsIEEESinglePrecisionFloatingPoint(code: float):
    sign = True if code < 0 else False
    code = abs(code)
    if code > 1:
        for i in range(1, 128):
            if 2 ** i > code:
                exponent = i-1
                break
    else:
        for i in range(1, 127):
            if 2 ** -i <= code:
                exponent = -i
                break
    remainder = code / 2 ** exponent
    if remainder >= 1:
        remainder -= 1
    mantiss = DecFractionToBinFraction(remainder, 23)
    return ('1 ' if sign else '0 ') +  '0' * (8 - len('{0:b}'.format(exponent + 127))) + '{0:b}'.format(exponent + 127) + ' ' +''.join(mantiss)


if __name__ == '__main__':
    print('Please enter the integer: ', end='')
    num = input()
    try:
        int(num)
    except Exception:
        print('Integer please!')
        exit(1)
    
    intNum = int(num)
    dataLen = 64
    if intNum > -128 and intNum <= 127:  
        dataLen = 8
    elif intNum > -32768 and intNum <= 32767:
        dataLen = 16
    elif intNum > -2147483648 and intNum <= 2147483647:
        dataLen = 32
  
    print('Representation in Sign-Magnitude format: ' + RepresentAsSignMagnitude(num, dataLen))
    print('Representation in 1st Complement format: ' + RepresentAsFirstComplement(num, dataLen))

    intNum = int(num)
    dataLen = 64
    if intNum >= -128 and intNum <= 127:  
        dataLen = 8
    elif intNum >= -32768 and intNum <= 32767:
        dataLen = 16
    elif intNum >= -2147483648 and intNum <= 2147483647:
        dataLen = 32

    print('Representation in 2nd Complement format: ' + RepresentAsSecondComplement(num, dataLen))

    print('Please enter the float: ', end='')
    num = input()
    print('Representation in binary floating point format:\n' + RepresentAsFloatingWithSignForMantissAndSignForExponent(float(num)))
    print('Representation in binary IEEE Single format:\n' + RepresentAsIEEESinglePrecisionFloatingPoint(float(num)))
