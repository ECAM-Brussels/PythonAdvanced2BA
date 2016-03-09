#!/usr/bin/env python3
# timeit.py
# author: Sébastien Combéfis
# version: March 9, 2016

import time

def timeit(f):
    def wrapper(*args):
        t1 = time.time()
        result = f(*args)
        print('Executed in {:.2f} seconds'.format(time.time() - t1))
        return result
    return wrapper

@timeit
def fact(n):
    i = 1
    result = 1
    while i <= n:
        result *= i
        i += 1
    return result

fact(1e5)