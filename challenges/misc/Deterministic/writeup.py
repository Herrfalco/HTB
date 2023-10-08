#!/usr/bin/env python3

START = '69420'
END = '999'

if __name__ == '__main__':
    routes = {}
    cur = START
    res = []

    with open('deterministic.txt', 'r') as file:
        for line in file.read().split('\n')[2:]:
            entry = line.split(' ')
            routes[entry[0]] = entry[1:]

    while cur != END:
        res += [int(routes[cur][0])]
        cur = routes[cur][1]

    for mod in range(2 ** 8):
        final = ''.join([chr(val ^ mod) for val in res])
        if 'HTB{' in final:
            print(final)
