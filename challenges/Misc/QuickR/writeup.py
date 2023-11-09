#!/usr/bin/env python3

from qreader import QReader
from PIL import Image
import numpy as np
import socket
import time
import sys
import re

if __name__ == '__main__':
    qreader = QReader()

    if len(sys.argv) != 2:
        print("Usage: ./writeup IP_ADRESS:PORT")
        exit(1)

    host, port = sys.argv[1].split(':');

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, int(port)))

    time.sleep(2)
    data = client.recv(102400).decode('utf-8')
    white = None
    canvas = []
    for line in data.split('\n'):
        pxs = re.findall("\[(\d+)m  ", line)
        if len(pxs) != 0:
            if not white:
                white = pxs[0]
            canvas += [[(255, 255, 255) if px == white else (0, 0, 0) for px in pxs]]
    array = np.array(canvas, dtype=np.uint8)
    img = Image.fromarray(array)
    img.show()
    client.send(bytes(str(eval(qreader.detect_and_decode(image=array)[0][:-3].replace('x', '*'))) + '\n', 'ascii'))
    time.sleep(2)
    data = client.recv(102400).decode('utf-8')
    print(data)
