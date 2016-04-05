#!/usr/bin/env python3
# symbolic.py
# author: Sébastien Combéfis
# version: April 5, 2016

from sympy import *

init_printing(use_unicode=True)

x, y = symbols('x y')

d = Derivative(2 * (x ** 3) + y * x ** 2 - 1, x)
expr1 = d.doit()

print(d)
print(expr1)
print(factor(expr1))

expr2 = expr1.subs(x, 10)
print(expr2)
print(solve(expr2, y))
print(integrate(expr2, y))