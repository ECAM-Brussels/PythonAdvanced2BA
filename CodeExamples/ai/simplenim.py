#!/usr/bin/env python3
# simplenim.py
# author: Sébastien Combéfis
# version: March 14, 2016

from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax

class SimpleNim(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.nplayer = 1
        self.__sticks = 5
    
    def possible_moves(self):
        return [str(v) for v in (1, 2, 3) if v <= self.__sticks]
    
    def make_move(self,move):
        self.__sticks -= int(move)
    
    def win(self):
        return self.__sticks <= 0
    
    def is_over(self):
        return self.win()
    
    def show(self):
        print('{} sticks left in the pile'.format(self.__sticks))
    
    def scoring(self):
        return 1 if self.win() else 0

ai = Negamax(13)
game = SimpleNim([Human_Player(), AI_Player(ai)])
history = game.play()