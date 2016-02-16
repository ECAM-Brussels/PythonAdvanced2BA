#!/usr/bin/env python3
# connectfour.py
# Author: Quentin Lurkin
# Version: February 16, 2016

import argparse
import sys
import random

from lib import game

class ConnectFourServer(game.GameServer):
    '''Class representing a server for the Connect Four game'''
    def __init__(self, verbose=False):
        super().__init__('Connect Four', 2, verbose=verbose)
        self.__state = [    # list of 7 columns with 6 places each
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None],
            [None, None, None, None, None, None]
        ]
    
    def applymove(self, move):
        try:
            move = int(move)
            if not (0 <= move < 7):
                raise game.InvalidMoveException('The move is outside of the board')
            if self.__state[move][-1] is not None:
                raise game.InvalidMoveException('The specified columns is full')
            self.__state[move][self.__state[move].index(None)] = self.currentplayer
        except:
            raise game.InvalidMoveException('A valid move must be an integer between 0 and 6')
    
    def winner(self):
        state = self.__state
        if self.turns >= 7:
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
            
            return -1
        elif self.turns == 6*7:
            return None
        return -1
    
    @property
    def state(self):
        return ' '.join([str(value) for row in self.__state for value in row])


class ConnectFourClient(game.GameClient):
    '''Class representing a client for the Connect Four game'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, verbose=verbose)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    def _nextmove(self, state):
        state = [None if value == 'None' else int(value) for value in state.split(' ')]
        state = [state[i*6:i*6+6] for i in range(7)]
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
    client_parser.add_argument('--host', help='hostname of the server (default: localhost)', default='localhost')
    client_parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    client_parser.add_argument('--verbose', action='store_true')
    # Parse the arguments of sys.args
    args = parser.parse_args()
    if args.component == 'server':
        ConnectFourServer(verbose=args.verbose).run()
    else:
        ConnectFourClient(args.name, (args.host, args.port), verbose=args.verbose)