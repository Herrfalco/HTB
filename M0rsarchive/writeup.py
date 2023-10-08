#!/usr/bin/env python3

import os
import time
from PIL import Image
from numpy import asarray

MORSE = { '.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '-.-.-.-': ' ', '--..--': ',', '---...': ':', '-.-.-.': ';', '.-.-.-': '.', '.-..-.': '"', '-----.': '(', '.-----': ')', '-.--.-': '\'', '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0' }

if __name__ == '__main__':
    count = 999

    while count >= 0:
        image = Image.open('pwd.png')
        data = asarray(image)
        bg = data[0][0]
        pswd = ''
        
        for line in data:
            code = ''
            sz = 0
            for px in line:
                if str(px) != str(bg):
                    sz += 1
                elif sz != 0:
                    code += '.' if sz == 1 else '-'
                    sz = 0
            if code:
                pswd += MORSE[code]
        os.system(f'unzip -qP {pswd} flag_{count}.zip;\
                rm -rf flag_{count}.zip pwd.png;')
        os.system('cat flag/flag' if count == 0 else 'mv flag/* .; rm -rf flag')
        count -= 1
