#!/usr/bin/env python3
# pylos.py
# Author: Quentin Lurkin
# Version: April 28, 2017

import argparse
import socket
import sys
import json

from lib import game

class PylosState(game.GameState):
    '''Class representing a state for the Pylos game.'''
    def __init__(self):
        
        # define a layer of the board
        def squareMatrix(size):
            matrix = []
            for i in range(size):
                matrix.push([None]*size)
            return matrix

        board = []
        for i in range(4):
            board.push(squareMatrix(4-i))

        initialstate = {
            'board': board,
            'dark': 15,
            'light': 15,
            'turn': 'light'
        }

        super().__init__(initialstate)
    
    # update the state with the move
    # raise game.InvalidMoveException
    def update(self, move, player):
        state = self._state['visible']

    # return 0 or 1 if a winner, return None if draw, return -1 if game continue
    def winner(self):
        state = self._state['visible']
        
    # print the state
    def prettyprint(self):
        state = self._state['visible']
        


class PylosServer(game.GameServer):
    '''Class representing a server for the Pylos game.'''
    def __init__(self, verbose=False):
        super().__init__('Pylos', 2, PylosState(), verbose=verbose)
    
    def applymove(self, move):
        self._state.update(move, self.currentplayer)


class TicTacToeClient(game.GameClient):
    '''Class representing a client for the Pylos game.'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, PylosState, verbose=verbose)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    #return move as string
    def _nextmove(self, state):
        ''' example of moves
        move = {
            'move': 'place',
            'to': [0,1,1]
        }

        move = {
            'move': 'move',
            'from': [0,1,1],
            'to': [1,1,1]
        }

        move = {
            'move': 'move',
            'from': [0,1,1],
            'to': [1,1,1]
            'remove': [
                [1,1,1],
                [1,1,2]
            ]
        }
        
        return it in JSON'''
        
        move = {}
        return json.dumps(move)


if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Pylos game')
    subparsers = parser.add_subparsers(description='server client', help='Pylos game components', dest='component')
    # Create the parser for the 'server' subcommand
    server_parser = subparsers.add_parser('server', help='launch a server')
    server_parser.add_argument('--host', help='hostname (default: localhost)', default='localhost')
    server_parser.add_argument('--port', help='port to listen on (default: 5000)', default=5000)
    server_parser.add_argument('--verbose', action='store_true')
    # Create the parser for the 'client' subcommand
    client_parser = subparsers.add_parser('client', help='launch a client')
    client_parser.add_argument('name', help='name of the player')
    client_parser.add_argument('--host', help='hostname of the server (default: localhost)', default='127.0.0.1')
    client_parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    client_parser.add_argument('--verbose', action='store_true')
    # Parse the arguments of sys.args
    args = parser.parse_args()
    if args.component == 'server':
        PylosServer(verbose=args.verbose).run()
    else:
        PylosClient(args.name, (args.host, args.port), verbose=args.verbose)