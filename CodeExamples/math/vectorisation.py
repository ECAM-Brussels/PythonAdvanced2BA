#!/usr/bin/env python3
# vectorisation.py
# author: Sébastien Combéfis
# version: April 6, 2016

import numpy as np

def add(a, b):
    return a + b

vec_add = np.vectorize(add)

x = [1, 2, 3]
y = [7, 8, 9]
print(vec_add(x, y))