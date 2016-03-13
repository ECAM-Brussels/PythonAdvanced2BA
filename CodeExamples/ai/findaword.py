#!/usr/bin/env python3
# findaword.py
# author: Sébastien Combéfis
# version: March 12, 2016

from simpleai.search import SearchProblem
from simpleai.search import breadth_first

GOAL = 'HELLO'

class HelloProblem(SearchProblem):
    def actions(self, state):
        if len(state) < len(GOAL):
            return list(' DEHLORW')
        return []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL

problem = HelloProblem(initial_state='')
result = breadth_first(problem)
print(result.state)
print(result.path())