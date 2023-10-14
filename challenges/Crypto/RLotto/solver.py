#!/usr/bin/env python3

import time
import random
from sys import argv

def take_five(seed=None):
    numbers = []

    if seed:
        random.seed(seed)
    while len(numbers) < 5:
        nb = random.randint(1, 90)
        if nb not in numbers:
            numbers.append(nb)
    return numbers

if __name__ == "__main__":
    target = []

    if len(argv) < 6:
        print('Error: need 5 different numbers from 1 to 90')
        exit(1)
    for arg in argv[1:]:
        try:
            nb = int(arg)
            if not 1 <= nb <= 90 or nb in target:
                raise ValueError
        except ValueError:
            print('Error: need 5 different numbers from 1 to 90')
            exit(2)
        target.append(nb)

    seed = int(time.time())

    count = 0
    while target != take_five(seed):
        seed -= 1
        count += 1
    print(count)
    print(take_five())
