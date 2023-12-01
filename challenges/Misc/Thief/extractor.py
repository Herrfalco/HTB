#!/usr/bin/env python3

from Crypto.Cipher import AES
from pyshark import FileCapture

KEY = b'The Bloodharbor!'

def idx_from_id_seq(id_nb, seq_nb):
    return 2 ** (id_nb - 1) - 1 + (-seq_nb - 1 + 2 ** (id_nb - 1) if id_nb % 2 else seq_nb)

if __name__ == "__main__":
    cap = FileCapture('challenge.pcap', \
            display_filter='ip.src == 192.168.127.146 \
            and ip.dst == 172.67.139.222 \
            and icmp.type == 8')
    result = [(idx_from_id_seq(int(pkt.icmp.ident), int(pkt.icmp.seq)), bytes.fromhex(pkt.icmp.data)[6:]) for pkt in cap]
    result.sort(key = lambda x: x[0])
    plain = []
    for _, data in result:
        iv = data[:16]
        data = data[16:]
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        plain.append(cipher.decrypt(data))
    with open('exfilt.png', 'wb') as out:
        out.write(b''.join(plain))
