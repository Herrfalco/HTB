#!/usr/bin/env python3

import pyperclip

if __name__ == "__main__":
    result = ''
    for line in pyperclip.paste().split('\n')[1:]:
        result += f"-H '{line}' "
    pyperclip.copy(result)
