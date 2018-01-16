import argparse
from pylos import PylosClient
import json
import copy
from functools import reduce


def findMoves(state):
    def allPositions():
        positions = []
        for layer in range(4):
            for row in range(4-layer):
                for column in range(4-layer):
                    positions.append((layer, row, column))
        return positions

    def allCouples(liste):
        couples = []
        for i in range(len(liste)):
            for j in range(i):
                couples.append([liste[i], liste[j]])
        return couples

    def mine(state, player):
        def f(pos):
            layer, row, column = pos
            return state.get(layer, row, column) == player
        return f

    def canMove(state):
        def f(pos):
            layer, row, column = pos
            try:
                state.canMove(layer, row, column)
            except:
                return False
            return True
        return f

    def validPosition(state):
        def f(pos):
            layer, row, column = pos
            try:
                state.validPosition(layer, row, column)
            except:
                return False
            return True
        return f

    def validMove(state):
        def f(move):
            newState = copy.deepcopy(state)
            try:
                newState.update(move, state._state['visible']['turn'])
            except:
                return False
            return True
        return f

    def checkSQuares(state):
        def f(moves, move):
            newState = copy.deepcopy(state)
            try:
                newState.update(move, state._state['visible']['turn'])
            except:
                #print('INVALID !!!!!')
                return moves

            #if move is None:
            #    print('AAAAAAAARRRRGGGGGGG!!!!!!!!!')
            moves.append(move)
            
            if newState.createSquare(move['to']):
                movables = list(filter(canMove(newState), list(filter(mine(newState, state._state['visible']['turn']), positions))))
                #print('movable (for remove):', movables)
                #print('allCouples (for remove):', allCouples(movables))
                #print('allSingles (for remove):', list(map(lambda x: [x], movables)))
                removables = allCouples(movables)
                removables.extend(list(map(lambda x: [x], movables)))
                #print('removables:', removables)
                #print('copy:', copy.copy(move).update({'remove': []}))
                #print('removes:', [dict(**move, remove=r) for r in removables])
                moves.extend([dict(**move, remove=r) for r in removables])
            
            return moves
        return f

    positions = allPositions()
    #print('positions:', positions)
    movables = list(filter(canMove(state), list(filter(mine(state, state._state['visible']['turn']), positions))))
    #print('movables:', movables)
    valids = list(filter(validPosition(state), positions))
    #print('valids:', valids)
    moves = [{'move': 'move', 'from': f, 'to':t} for f in movables for t in valids]
    #print('moves (1):', moves)
    moves.extend([{'move': 'place', 'to': t} for t in valids])
    #print('moves (2):', moves)
    moves = reduce(checkSQuares(state) ,moves,[])
    #print('moves (final):', moves)

    return sorted(moves, key=lambda move: -((1 if move['move'] == 'move' else 0) + (len(move['remove']) if 'remove' in move else 0)))


class RobotPylos(PylosClient):
    def __init__(self, name, server, verbose=False):
        super().__init__(name, server, verbose=verbose)

    def _nextmove(self, state):
        moves = findMoves(state)
        return json.dumps(moves[0])


if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Pylos game')
    
    parser.add_argument('name', help='name of the player')
    parser.add_argument('--host', help='hostname of the server (default: localhost)', default='127.0.0.1')
    parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    parser.add_argument('--verbose', action='store_true')
    
    # Parse the arguments of sys.args
    args = parser.parse_args()
    RobotPylos(args.name, (args.host, args.port), verbose=args.verbose)