#!/usr/bin/env python3
# tictactoe.py
# Author: Sébastien Combéfis
# Version: February 12, 2016

import argparse
import sys

from lib import game

class TicTacToeServer(game.GameServer):
    def __init__(self):
        super().__init__('Tic-tac-toe', 1)
        self.__state = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def applymove(self, move):
        if not (type(move) == tuple and len(move) == 2):
            raise game.InvalidMoveException('A valid move must be a two-element tuple')
        if not (0 <= move[0] <= 2 and 0 <= move[1] <= 2):
            raise game.InvalidMoveException('The move is outside of the board')
        if self.__state[move[0]][move[1]] is None:
            raise game.InvalidMoveException('The specified cell is not empty')
        self.__state[move[0]][move[1]] = self.currentplayer
    
    def isfinished(self):
        return self.turns == 9
    
    @property
    def state(self):
        return ' '.join([str(value) for row in self.__state for value in row])


class TicTacToeClient(game.GameClient):
    def __init__(self, name, server):
        super().__init__(server)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    def _nextmove(self, state):
        pass

if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Tic-tac-toe game')
    subparsers = parser.add_subparsers(description='server client', help='Tic-tac-toe game components', dest='component')
    # Create the parser for the 'server' subcommand
    server_parser = subparsers.add_parser('server', help='launch a server')
    server_parser.add_argument('--host', help='hostname (default: localhost)', default='localhost')
    server_parser.add_argument('--port', help='port to listen on (default: 5000)', default=5000)
    # Create the parser for the 'client' subcommand
    client_parser = subparsers.add_parser('client', help='launch a client')
    client_parser.add_argument('name', help='name of the player')
    client_parser.add_argument('--host', help='hostname of the server (default: localhost)', default='localhost')
    client_parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    # Parse the arguments of sys.args
    args = parser.parse_args()
    if args.component == 'server':
        TicTacToeServer().run()
    else:
        TicTacToeClient(args.name, (args.host, args.port))