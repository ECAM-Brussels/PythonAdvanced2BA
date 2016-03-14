#!/usr/bin/env python3
# simplenim.py
# author: Sébastien Combéfis
# version: March 14, 2016

from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax

class SimpleNim(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.pile = 5
        self.nplayer = 1
    
    def possible_moves(self):
        return ['1', '2', '3']
    
    def make_move(self,move):
        self.pile -= int(move)
    
    def win(self):
        return self.pile <= 0
    
    def is_over(self):
        return self.win()
    
    def show(self):
        print('{} sticks left in the pile'.format(self.pile))
    
    def scoring(self):
        return 1 if self.win() else 0

ai = Negamax(13)
game = SimpleNim([Human_Player(), AI_Player(ai)])
history = game.play()