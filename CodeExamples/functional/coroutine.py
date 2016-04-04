#!/usr/bin/env python3
# coroutine.py
# author: Sébastien Combéfis
# version: April 4, 2016

def coroutine(f):
    def primer(*args, **kwargs):
        g = f(*args, **kwargs)
        next(g)
        return g
    return primer

@coroutine
def summer():
    total = 0
    while True:
        value = yield total
        total += value

s = summer()

print(s.send(12))
print(s.send(3))
print(s.send(5))