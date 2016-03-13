#!/usr/bin/env python3
# findaword.py
# author: Sébastien Combéfis
# version: March 12, 2016

import time

from simpleai.search import SearchProblem
from simpleai.search import breadth_first
from simpleai.search import greedy

GOAL = 'HELLO'

class HelloProblem(SearchProblem):
    def actions(self, state):
        if len(state) < len(GOAL):
            return list(' ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return []

    def result(self, state, action):
        return state + action

    def is_goal(self, state):
        return state == GOAL
    
    def heuristic(self, state):
        wrong = sum([1 if state[i] != GOAL[i] else 0 for i in range(len(state))])
        missing = len(GOAL) - len(state)
        return wrong + missing

# Using Breadth-First Search
t1 = time.time()
problem = HelloProblem(initial_state='')
result = breadth_first(problem)
print('Time: {:.5f}s'.format(time.time() - t1))
print(result.state)
print(result.path())

# Using Greedy Search
t1 = time.time()
problem = HelloProblem(initial_state='')
result = greedy(problem)
print('Time: {:.5f}s'.format(time.time() - t1))
print(result.state)
print(result.path())