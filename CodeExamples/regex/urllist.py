#!/usr/bin/env python3
# urllist.py
# author: Sébastien Combéfis
# version: February 25, 2016

import re
import sys
import urllib.request

if len(sys.argv) == 2:
    with urllib.request.urlopen(sys.argv[1]) as response:
        data = response.read().decode()
        pattern = re.compile(r'<a.*href="(.*?)".*>')
        for match in pattern.finditer(data):
            print(match.group(1))