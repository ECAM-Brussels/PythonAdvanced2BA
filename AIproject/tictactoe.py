# tictactoe.py
# Author: Sébastien Combéfis
# Version: February 8, 2016

from lib import game

class TicTacToe(game.Game):
    def __init__(self):
        super().__init__('Tic-tac-toe', 2)

if __name__ == '__main__':
    t = TicTacToe()
    print(t.name)