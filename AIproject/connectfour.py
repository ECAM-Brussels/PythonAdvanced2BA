#!/usr/bin/env python3
# connectfour.py
# Author: Quentin Lurkin
# Version: February 16, 2016

import argparse
import sys
import random

from lib import game

class ConnectFourState(game.GameState):
    '''Class representing a state for the Connect Four game.'''
    def __init__(self, initialstate = [[None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6, [None] * 6]):
        super().__init__(initialstate)

    def update(self, move, player):
        state = self._state['visible']
        try:
            move = int(move)
        except:
            raise game.InvalidMoveException('A valid move must be an integer between 0 and 6')
        else:
            if not (0 <= move < 7):
                raise game.InvalidMoveException('The move is outside of the board')
            if state[move][-1] is not None:
                raise game.InvalidMoveException('The specified columns is full')
            state[move][state[move].index(None)] = player

    def winner(self):
        state = self._state['visible']

        # check columns
        for c in range(7):
            for r in range(3):
                if state[c][r] is not None and all(elem == state[c][r] for elem in [state[c][r+i] for i in range(4)]):
                    return state[c][r]

        # check rows
        for c in range(4):
            for r in range(6):
                if state[c][r] is not None and all(elem == state[c][r] for elem in [state[c+i][r] for i in range(4)]):
                    return state[c][r]
        
        # check diagonal
        for c in range(4):
            for r in range(3):
                if state[c][r] is not None and all(elem == state[c][r] for elem in [state[c+i][r+i] for i in range(4)]):
                    return state[c][r]
        
        # check other diagonal
        for c in range(3,7):
            for r in range(3):
                if state[c][r] is not None and all(elem == state[c][r] for elem in [state[c-i][r+i] for i in range(4)]):
                    return state[c][r]

        # board is full   
        if all(map(lambda column: column[-1] != None, state)):
            return None

        return -1
    
    def prettyprint(self):
        state = self._state['visible']
        print('\n'.join(['|'.join(list(map(lambda column : '_' if column[row] == None else str(column[row]), state))) for row in range(5, -1, -1)]))
        

class ConnectFourServer(game.GameServer):
    '''Class representing a server for the Connect Four game'''
    def __init__(self, verbose=False):
        super().__init__('Connect Four', 2, ConnectFourState(), verbose=verbose)
    
    def applymove(self, move):
        self._state.update(move, self.currentplayer)


class ConnectFourClient(game.GameClient):
    '''Class representing a client for the Connect Four game'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, ConnectFourState, verbose=verbose)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    def _nextmove(self, state):
        state = state._state['visible']
        random.seed()
        move = random.randrange(7)
        while state[move][-1] != None:
            move = random.randrange(7)
        return str(move)


if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Connect Four game')
    subparsers = parser.add_subparsers(description='server client', help='Connect four game components', dest='component')
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
        ConnectFourServer(verbose=args.verbose).run()
    else:
        ConnectFourClient(args.name, (args.host, args.port), verbose=args.verbose)