#!/usr/bin/env python3
# summer.py
# author: Sébastien Combéfis
# version: April 4, 2016

def summer():
    total = 0
    while True:
        value = yield total
        total += value

s = summer()
next(s)

print(s.send(12))
print(s.send(3))
print(s.send(5))