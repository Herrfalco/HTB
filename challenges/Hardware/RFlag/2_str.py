#!/usr/bin/env python3

import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: 2_str.py HEX_DATA')
        exit(1)

    for val in sys.argv[1:]:
        print(chr(int(val, 16)), end='')
