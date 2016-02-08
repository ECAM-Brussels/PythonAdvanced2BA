# game.py
# Author: Sébastien Combéfis
# Version: February 8, 2016

class Game():
    def __init__(self, name, nbplayers):
        self.__name = name
        self.__nbplayers = nbplayers
    
    @property
    def name(self):
        return self.__name
    
    @property
    def nbplayers(self):
        return self.__nbplayers