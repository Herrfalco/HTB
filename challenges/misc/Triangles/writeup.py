#!/usr/bin/env python3

from collections import namedtuple
import csv
import math

Point = namedtuple('Point', 'x y')

PREC = 0.001

def cap(num):
    if num > 99:
        return 99
    if num < 0:
        return 0
    return num

def cust_round(val):
    if math.ceil(val) - val < PREC:
        return float(math.ceil(val))
    elif val - math.floor(val) < PREC:
        return float(math.floor(val))
    return val

def circle_points(center, r):
    res = []

    for x in range(cap(math.ceil(center.x - r)), cap(math.floor(center.x + r)) + 1):
        y1 = cust_round(center.y + math.sqrt(pow(r, 2) - pow(x - center.x, 2)))
        y2 = cust_round(center.y - math.sqrt(pow(r, 2) - pow(x - center.x, 2)))
        if y1.is_integer() and 0 <= y1 < 100:
            res.append(Point(x, int(y1)))
        if y2.is_integer() and 0 <= y2 < 100:
            res.append(Point(x, int(y2)))
    return res

if __name__ == "__main__":
    table = []
    dic = {}
    with open('grid.csv') as grid:
        for y, row in enumerate(csv.reader(grid)):
            table.append(row)
            for x, cell in enumerate(row):
                if not cell in dic:
                    dic[cell] = []
                dic[cell].append(Point(x, y))

    with open('out.csv') as out:
        while True:
            sym = ['\0'] * 3
            targ_d = [0.] * 3
            next_d = [0.] * 3

            for i in range(3):
                try:
                    sym[i], targ_d[i] = out.readline().strip().split(',')
                except ValueError:
                    print()
                    exit(0)
                targ_d[i] = float(targ_d[i])
            for i in range(3):
                next_d[i] = out.readline().strip().split(',')[1]
                next_d[i] = float(next_d[i])

            a, b, c = None, None, None
            for p0 in dic[sym[0]]:
                for p1 in circle_points(p0, next_d[0]):
                    if table[p1.y][p1.x] != sym[1]:
                        continue
                    for p2 in circle_points(p1, next_d[1]):
                        if table[p2.y][p2.x] != sym[2]:
                            continue
                        for p3 in circle_points(p2, next_d[2]):
                            if p3 != p0:
                                continue
                            a = p0
                            b = p1
                            c = p2
                            break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break;
            else:
                print("Error: Triangle not found")
                exit(1)
            
            for p0 in circle_points(a, targ_d[0]):
                for p1 in circle_points(b, targ_d[1]):
                    for p2 in circle_points(c, targ_d[2]):
                        if p0 == p1 and p1 == p2:
                            print(table[p0.y][p0.x], end='')
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                print("Error: Can't find position")
                exit(2)
