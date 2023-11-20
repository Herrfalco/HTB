#!/usr/bin/env python3

import string

CHARS = '012345678910abcdefghijklmnopqrstuvwxyz-_!?{}'

if __name__ == '__main__':
    result = []

    with open('msg.enc', 'r') as file:
        for b in bytes.fromhex(file.read()):
            for c in CHARS:
                if (123 * ord(c) + 18) % 256 == b:
                    print(c, end='')
                    break
