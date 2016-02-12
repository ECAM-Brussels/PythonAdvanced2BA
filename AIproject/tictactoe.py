#!/usr/bin/env python3
# tictactoe.py
# Author: Sébastien Combéfis
# Version: February 12, 2016

import sys
from lib import game

class TicTacToeServer(game.GameServer):
    def __init__(self):
        super().__init__('Tic-tac-toe', 2)
        self.__state = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def applymove(self, move):
        if not (type(move) == tuple and len(move) == 2):
            raise InvalidMoveException('A valid move must be a two-element tuple')
        if not (0 <= move[0] <= 2 and 0 <= move[1] <= 2):
            raise InvalidMoveException('The move is outside of the board')
        if self.__state[move[0]][move[1]] is None:
            raise InvalidMoveException('The specified cell is not empty')
        self.__state[move[0]][move[1]] = self.currentplayer
    
    def isfinished(self):
        return self.turns == 9


class TicTacToeClient(game.GameClient):
    def __init__(self, server):
        super().__init__(server)

if __name__ == '__main__':
    t = TicTacToeServer()
    t.run()