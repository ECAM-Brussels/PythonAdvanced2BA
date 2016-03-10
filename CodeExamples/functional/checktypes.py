#!/usr/bin/env python3
# checktypes.py
# author: Sébastien Combéfis
# version: March 10, 2016

def checktypes(*types):
    def decorator(f):
        print(types, len(types))
        def wrapper(*args):
            assert len(types) == len(args), 'wrong number of types'
            print(args, len(args))
            for (a, t) in zip(args, types):
                assert isinstance(a, t), 'arg {} does not match {}'.format(a, t)
            return f(*args)
        return wrapper
    return decorator

@checktypes(int)
def compute(n):
    return n ** 2

print(compute(9))