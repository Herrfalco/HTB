#!/usr/bin/env python3

import socket
import time
import sys

def rec_fn(data):
    nest = 0
    start = None
    new_data = []
    for i, val in enumerate(data):
        if '(' in val:
            if nest == 0:
                data[i] = data[i][1:]
                start = i
            nest += val.count('(')
        elif ')' in val:
            nest -= val.count(')')
            if nest == 0:
                data[i] = data[i][:-1]
                new_data += rec_fn(data[start:i+1])
        elif nest == 0:
            new_data += [data[i]]
    new_data = [eval(x) for x in "".join(new_data).split('*')]
    res = 1
    for dat in new_data:
        res *= int(dat)
    return [str(res)]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./writeup IP_ADRESS:PORT")
        exit(1)
    host, port = sys.argv[1].split(':');

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, int(port)))

    while True:
        data = client.recv(4096).decode('utf-8')
        seq = None
        for line in data.split('\n'):
            if not line:
                continue
            print(line)
            if line[0] == '[':
                seq = line.split(' ')[1:-2]
                break
        else:
            break
        resp = rec_fn(seq)[0] + '\n'
        client.send(bytes(resp, 'utf-8'))
    client.close()
