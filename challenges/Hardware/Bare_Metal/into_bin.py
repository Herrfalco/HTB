#!/usr/bin/env python3

import binascii 
from itertools import islice

START = 0x46 * 2
END = 0x466 * 2

# Start Code: 1 byte symbol ':'
# Byte Count: 1 byte data size
# Address: 2 bytes memory address.
# Record Type: 1 byte value type (00: Data, 01: EOF)
# Data: ...
# Checksum: 1 byte checksum

# Disassemble with ghidra/ATMega328p

if __name__ == "__main__":
    data = b''
    with open('extracted_firmware.hex', 'r') as file:
        for line in file:
            data += bytes.fromhex(line[9:-3])

    data = ''.join((str(int(x == 0x9a)) for x in data[START+1:END:6]))
    while len(data):
        byte = data[:8]
        print(chr(int(byte, 2)), end='')
        data = data[8:]
