#!/usr/bin/env python3

import re

if __name__ == '__main__':
    res = ""

    with open('js/login.js', 'r') as file:
        vals = re.findall("0x([0-9a-fA-F]+)", file.read())
    for v in vals:
        v = int(v, 16)
        try:
            res += chr(v)
        except ValueError:
            continue
    print(re.findall("HTB{.+}", res)[0])
