#!/usr/bin/env python3

from pyshark import FileCapture
from base64 import b64decode
from itertools import cycle
from zlib import decompress
import re

KEY = b"80e32263"
HDR = b"6f8af44abea0"
FTR = b"351039f4a7b5"
OUT = 'pwdb.kdbx'

def dec_xor(data) :
    return bytes(x ^ y for x, y in zip(data, cycle(KEY)))

if __name__ == '__main__':
    cap = FileCapture('19-05-21_22532255.pcap', display_filter='http and ip.addr == 10.132.0.2 and ip.addr == 23.129.64.207')
    result = None
    for pkt in cap:
        match = re.search(HDR + b'.+' + FTR, bytes.fromhex(pkt.http.file_data.replace(':', '')))
        result = b64decode(match[0][len(HDR):-len(FTR)] + b'====')
        result = dec_xor(result)
        result = decompress(result)
        print(str(result, 'utf-8').replace(';', '\n'))
    with open(OUT, 'wb') as out:
        out.write(b64decode(result))
    print('\n>>> pwdb.kdbx file extracted <<<')
