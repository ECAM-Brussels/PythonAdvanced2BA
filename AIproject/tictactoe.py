#!/usr/bin/env python3
# tictactoe.py
# Author: Sébastien Combéfis
# Version: March 28, 2016

import argparse
import socket
import sys

from lib import game

class TicTacToeState(game.GameState):
    '''Class representing a state for the Tic-tac-toe game.'''
    def __init__(self, initialstate=[None] * 9):
        super().__init__(initialstate)
    
    def update(self, coord, player):
        state = self._state['visible']
        line, column = coord
        index = 3 * line + column
        if not (0 <= line <= 2 and 0 <= column <= 2):
            raise game.InvalidMoveException('The move is outside of the board')
        if state[index] is not None:
            raise game.InvalidMoveException('The specified cell is not empty')
        state[index] = player
    
    def _checkelems(self, state, elems):
        return state is not None and all(e == state for e in elems)
    
    def winner(self):
        state = self._state['visible']
        # Check horizontal and vertical lines
        for i in range(3):
            if self._checkelems(state[3 * i], [state[3 * i + e] for e in range(3)]):
                return state[3 * i]
            if self._checkelems(state[i], [state[3 * e + i] for e in range(3)]):
                return state[i]
        # Check diagonals
        if self._checkelems(state[0], [state[4 * e] for e in range(3)]):
            return state[0]
        if self._checkelems(state[2], [state[6 - 2 * e] for e in range(3)]):
            return state[2]
        return None if state.count(None) == 0 else -1
    
    def prettyprint(self):
        data = ['X' if e == 0 else 'O' if e == 1 else '_' for e in self._state['visible']]
        result = ''
        for i in range(3):
            result += '   {}\n'.format(' '.join(data[i * 3:i * 3 + 3]))
        print(result[:-1])


class TicTacToeServer(game.GameServer):
    '''Class representing a server for the Tic-tac-toe game.'''
    def __init__(self, verbose=False):
        super().__init__('Tic-tac-toe', 2, TicTacToeState(), verbose=verbose)
    
    def applymove(self, move):
        try:
            index = int(move)
            self._state.update((index // 3, index % 3), self.currentplayer)
        except:
            raise game.InvalidMoveException('A valid move must be a two-integer tuple')


class TicTacToeClient(game.GameClient):
    '''Class representing a client for the Tic-tac-toe game.'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, TicTacToeState, verbose=verbose)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    def _nextmove(self, state):
        return str(state._state['visible'].index(None))


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
    client_parser.add_argument('--host', help='hostname of the server (default: localhost)', default=socket.gethostbyname(socket.gethostname()))
    client_parser.add_argument('--port', help='port of the server (default: 5000)', default=5000)
    client_parser.add_argument('--verbose', action='store_true')
    # Parse the arguments of sys.args
    args = parser.parse_args()
    if args.component == 'server':
        TicTacToeServer(verbose=args.verbose).run()
    else:
        TicTacToeClient(args.name, (args.host, args.port), verbose=args.verbose)