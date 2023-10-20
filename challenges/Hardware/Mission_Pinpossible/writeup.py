#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""Error:
        1) Open capture file with Logic 1 (SALELAE)
        2) Create export i2c 8bits analyzer
        3) Specify output file as writeup argument""")
        exit(1)

    cap = None
    with open(sys.argv[1], 'r') as file:
        cap = bytes.fromhex(''.join([line.split(',')[3][2:] for line in file][1:]))
    buff = 0
    state = 'up'
    data = bytearray()
    for val in cap:
        if val & 0x5 != 0x5:
            continue
        if state == 'up':
            buff = val & 0xf0
            state = 'low'
        else:
            buff |= val >> 4
            data.append(buff)
            state = 'up'
    prev = None
    for c in data.decode():
        if c == 'H' or (prev == '*' and c != '*'):
            print(c, end='')
        prev = c
