# tictactoe.py
# Author: Sébastien Combéfis
# Version: February 8, 2016

from lib import game

class TicTacToe(game.Game):
    def __init__(self):
        super().__init__('Tic-tac-toe', 2)
        self.__state = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def isvalid(self, move):
        pass
    
    def isfinished(self):
        pass

if __name__ == '__main__':
    t = TicTacToe()
    t.run()