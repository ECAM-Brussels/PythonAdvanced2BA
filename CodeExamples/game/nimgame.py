#!/usr/bin/env python3
# nimgame.py
# author: Sébastien Combéfis
# version: February 28, 2016

def isgameover(state):
    for n in state:
        if n > 0:
            return False
    return True

def getmoves(state):
    moves = []
    for i in range(len(state)):
        moves += [(i, n) for n in range(1, state[i] + 1)]
    return moves

def isbadposition(state):
    if isgameover(state):
        return True
    return findgoodmove(state) is None

def findgoodmove(state):
    for move in getmoves(state):
        nextstate = tuple(state[i] - move[1] if i == move[0] else state[i] for i in range(len(state)))
        if isbadposition(nextstate):
            return move
    return None