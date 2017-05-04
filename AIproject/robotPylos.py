import argparse
from pylos import PylosClient
import json
import copy

class RobotPylos(PylosClient):
    def __init__(self, name, server, verbose=False):
        super().__init__(name, server, verbose=verbose)

    def allPositions(self):
        positions = []
        for layer in range(4):
            for row in range(4-layer):
                for column in range(4-layer):
                    positions.append([layer, row, column])
        return positions

    def allCouples(self):
        positions = self.allPositions()
        couples = []
        for i in range(len(positions)):
            for j in range(i):
                couples.append([positions[i], positions[j]])
        return couples

    def findMoves(self, state):
        moves = []
        positions = self.allPositions()
        removes = self.allCouples()
        removes += positions[:]
        removes.append([])

        for f in positions:
            for t in positions:
                move = {
                    'move': 'move',
                    'from': f,
                    'to': t
                }
                try:
                    newState = copy.deepcopy(state)
                    newState.update(move, state._state['visible']['turn'])
                    moves.append(move)
                except:
                    pass

        for t in positions:
            move = {
                'move': 'place',
                'to': t
            }
            try:
                newState = copy.deepcopy(state)
                newState.update(move, state._state['visible']['turn'])
                moves.append(move)
            except:
                pass

        return moves

    def _nextmove(self, state):
        moves = self.findMoves(state)
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