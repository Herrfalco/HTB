#!/usr/bin/env python3

import pyshark

VALS = "abcdefghijklmnopqrstuvwxyz1234567890\nXX\t -=[]\X;',./*-+X1234567890."
VALS_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()\nXX\t _+{}|X:~<>?*-+X1234567890."

if __name__ == '__main__':
    f = pyshark.FileCapture('mitm.log', display_filter="btl2cap")
    keys = []

    for p in f:
        data = p['btl2cap'].payload.split(":")
        if int(data[1], 16) != 1:
            continue
        key = [int(x, 16) - 4 for x in data[4:] if int(x, 16) >= 4 and int(x, 16) < len(VALS) + 4]
        if not key:
            continue
        keys += [(bool(int(data[2], 16)), key[0])]

    for maj, key in keys:
        print(VALS_UP[key] if maj else VALS[key], end='')
