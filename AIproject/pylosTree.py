from pylos import PylosState
from robotPylos import findMoves
import copy
import json

count = 0
total = len(findMoves(PylosState()))
print(count, '/', total)

def createTree(state, prof=0):
    global count
    #tree = Tree(state._state['visible'])
    tree = {
        'state': state._state['visible'],
        'children': []
    }

    moves = findMoves(state)
    moves = moves[0:4]
    if prof > 5:
        moves = []
    
    for move in moves:
        nextState = copy.deepcopy(state)
        nextState.update(move, state._state['visible']['turn'])
        subTree = createTree(nextState, prof+1)
        subTree['move'] = move
        tree['children'].append(subTree)
        if prof == 0:
            count+=1
            print(count, '/', total)
    return tree


tree = createTree(PylosState())

with open('pylos_tree.json', 'w') as file:
    json.dump(tree, file)