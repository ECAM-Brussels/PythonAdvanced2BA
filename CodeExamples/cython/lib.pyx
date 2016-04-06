# mylib.pyx
# author: Sébastien Combéfis
# version: April 6, 2016

cdef extern from "utils.h":
    cdef int cfact (int)
    cdef int csum (int, int)

def fact(n):
    return cfact(n)

def sum(a, b):
    return csum(a, b)