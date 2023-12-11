#!/usr/bin/env python3

if __name__ == "__main__":
    codes = []
    data = None

    i = 1
    while i < 2 ** 16:
        codes.append(i)
        i <<= 1

    print(codes)
    with open('out.txt', 'r') as file:
        data = [(int(a), int(b)) for a, b in (x.rstrip().split(' ') for x in file)]

    print(data)
    result = []
    for a, b in data:
        for key in range(0, 2 ** 16):
            if a ^ key in codes and b ^ key in codes:
                c = chr((codes.index(a ^ key) << 4) | codes.index(b ^ key))
                if ord(' ') <= ord(c) <= ord('~'):
                    print(c, end='')
        print()

#HTB{I_L0v3_VHDL_but_LOve_my_5w33thear7_m0re}
