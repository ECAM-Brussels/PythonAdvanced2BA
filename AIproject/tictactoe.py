#!/usr/bin/env python3
# tictactoe.py
# Author: Sébastien Combéfis
# Version: February 12, 2016

import argparse
import sys

from lib import game

class TicTacToeServer(game.GameServer):
    def __init__(self, verbose=False):
        super().__init__('Tic-tac-toe', 2, verbose=verbose)
        self.__state = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def applymove(self, move):
        try:
            index = int(move)
            move = (index // 3, index % 3)
            if not (0 <= move[0] <= 2 and 0 <= move[1] <= 2):
                raise game.InvalidMoveException('The move is outside of the board')
            if self.__state[move[0]][move[1]] is not None:
                raise game.InvalidMoveException('The specified cell is not empty')
            self.__state[move[0]][move[1]] = self.currentplayer
        except Exception as e:
            print(e)
            raise game.InvalidMoveException('A valid move must be a two-integer tuple')
    
    def winner(self):
        state = self.__state
        if self.turns >= 5:
            # Check horizontal and vertical lines
            for i in range(3):
                if state[i][0] is not None and all(elem == state[i][0] for elem in state[i]):
                    return state[i][0]
                if state[0][i] is not None and all(elem == state[0][i] for elem in [state[e][i] for e in range(3)]):
                    return state[0][i]
            # Check diagonals
            if state[0][0] is not None and all(elem == state[0][0] for elem in [state[e][e] for e in range(3)]):
                return state[0][0]
            if state[0][2] is not None and all(elem == state[0][2] for elem in [state[2-e][e] for e in range(3)]):
                return state[0][2]
            return -1
        elif self.turns == 9:
            return None
        return -1
    
    @property
    def state(self):
        return ' '.join([str(value) for row in self.__state for value in row])


class TicTacToeClient(game.GameClient):
    def __init__(self, name, server, verbose=False):
        super().__init__(server, verbose=verbose)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    def _nextmove(self, state):
        state = [None if value == 'None' else int(value) for value in state.split(' ')]
        return str(state.index(None))

if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Tic-tac-toe game')
    subparsers = parser.add_subparsers(description='server client', help='Tic-tac-toe game components', dest='component')
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
        TicTacToeServer(verbose=args.verbose).run()
    else:
        TicTacToeClient(args.name, (args.host, args.port), verbose=args.verbose)