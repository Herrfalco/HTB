#!/usr/bin/env python3

X_BITS = [ 9, 8, 14, 7, 3, 1, 0, 4 ]

if __name__ == "__main__":
    with open('traces.csv', 'r') as file:
        next(file)
        for i, line in enumerate(file):
            data = line[:-1].split(',')[1:]
            print(''.join([(' ' if data[bit] == '1' else 'X') for bit in X_BITS]))
            if not (i + 1) % 8:
                print()
