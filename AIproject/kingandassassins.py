#!/usr/bin/env python3
# kingandassassins.py
# Author: Sébastien Combéfis
# Version: March 27, 2016

import argparse
import sys

from lib import game

CARDS = {
    # (PA King, PA Knight, Cuff, PA Population/Assassins
    (1, 6, True, 5),
    (1, 5, False, 4),
    (1, 6, True, 5),
    (1, 6, True, 5),
    (1, 5, True, 4),
    (1, 5, False, 4),
    (2, 7, False, 5),
    (2, 7, False, 4),
    (1, 6, True, 5),
    (1, 6, True, 5),
    (2, 7, False, 5),
    (2, 5, False, 4),
    (1, 5, True, 5),
    (1, 5, False, 4),
    (1, 5, False, 4)
}
POPULATION = {'monk', 'plumwoman', 'appleman', 'hooker', 'fishwoman', 'butcher', 'blacksmith', 'shepherd', 'squire', 'carpenter', 'witchhunter', 'farmer'}
BOARD = (
    ('R', 'R', 'R', 'R', 'R', 'G', 'G', 'R', 'R', 'R'),
    ('R', 'R', 'R', 'R', 'R', 'G', 'G', 'R', 'R', 'R'),
    ('R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'R'),
    ('R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G'),
    ('R', 'G', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'),
    ('G', 'G', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'),
    ('R', 'R', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'),
    ('R', 'R', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'),
    ('R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G'),
    ('R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G')
)
PEOPLE = [[None for column in range(10)] for row in range(10)]
KNIGHTS = {(1, 3), (3, 0), (7, 8), (8, 7), (8, 8), (8, 9), (9, 8)}
VILLAGERS = {(1, 7), (2, 1), (3, 4), (3, 6), (5, 2), (5, 5), (5, 7), (5, 9), (7, 1), (7, 5), (8, 3), (9, 5)}
PEOPLE[9][9] = 'king'
for coord in KNIGHTS:
    PEOPLE[coord[0]][coord[1]] = 'knight'
for villager, coord in zip(POPULATION, VILLAGERS):
    PEOPLE[coord[0]][coord[1]] = villager
KA_INITIAL_STATE = {}

class KingAndAssassinsState(game.GameState):
    '''Class representing a state for the King & Assassins game.'''
    def __init__(self, initialstate=KA_INITIAL_STATE):
        super().__init__(initialstate)
    
    def update(self, moves, player):
        pass
    
    def winner(self):
        state = self._state['state']
        pass
    
    def prettyprint(self):
        pass


class KingAndAssassinsServer(game.GameServer):
    '''Class representing a server for the King & Assassins game'''
    def __init__(self, verbose=False):
        super().__init__('King & Assassins', 2, KingAndAssassinsState(), verbose=verbose)
    
    def applymove(self, move):
        pass


class KingAndAssassinsClient(game.GameClient):
    '''Class representing a client for the King & Assassins game'''
    def __init__(self, name, server, verbose=False):
        super().__init__(server, KingAndAssassinsState, verbose=verbose)
        self.__name = name
    
    def _handle(self, message):
        pass
    
    def _nextmove(self, state):
        pass


if __name__ == '__main__':
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='King & Assassins game')
    subparsers = parser.add_subparsers(description='server client', help='King & Assassins game components', dest='component')
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
        KingAndAssassinsServer(verbose=args.verbose).run()
    else:
        KingAndAssassinsClient(args.name, (args.host, args.port), verbose=args.verbose)