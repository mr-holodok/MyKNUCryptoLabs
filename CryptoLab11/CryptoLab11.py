
def get_MAC(msg:str, synchro:int, key:int) -> int:
    # we transform msg to cp1251, which is 8-bit 
    # so for creating blocks of len 64 bits we need 8 chars
    msg_blocks = [ msg[i:i+8] for i in range(0, len(msg), 8)]
    mac = synchro
    for block in msg_blocks:
        mac = mac ^ encode_block(block) 
        mac = mac ^ key
    return mac


def encode_block(block: str) -> int:
    concat = str();
    hex = lambda x: "{0:#0{1}b}".format(x, 10)[2:]

    for ch in block:
        concat += hex(int.from_bytes(ch.encode('cp1251'), 'little'));
    if len(block) < 8:
        concat += (8 - len(block)) * '00000000'
    return int(concat, 2)


if __name__ == "__main__":
    print("Please, enter message to be MAC-calculated:")
    msg = input()
    # synchro = 0b101010..10 (64-bit len)
    synchro = 12297829382473034410
    key = 1234
    print('MAC-code of message is: ' + str(get_MAC(msg, synchro, key)))
