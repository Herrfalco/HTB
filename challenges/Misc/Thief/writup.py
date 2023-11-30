#!/usr/bin/env python3

from Crypto.Cipher import AES
from pyshark import FileCapture

KEY = b'The Bloodharbor!'

def idx_from_id_seq(id_nb, seq_nb):
    return 2 ** (id_nb - 1) - 1 + (-seq_nb - 1 + 2 ** (id_nb - 1) if id_nb % 2 else seq_nb)

if __name__ == "__main__":
    print(idx_from_id_seq(1, 0))
    cap = FileCapture('challenge.pcap', \
            display_filter='icmp and ip.dst == 172.67.139.222')
    for pkt in cap:
        print(idx_from_id_seq(pkt.icmp.seq, pkt.icmp.ident))
        #data = bytes.fromhex(pkt.icmp.data)[6:]
        #iv = data[:16]
        #data = data[16:]
        #cipher = AES.new(KEY, AES.MODE_CBC, iv)
        #print(cipher.decrypt(data))
