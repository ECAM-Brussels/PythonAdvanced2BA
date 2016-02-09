# game.py
# Author: Sébastien Combéfis
# Version: February 8, 2016

from abc import *
import socket

class Game(metaclass=ABCMeta):
    def __init__(self, name, nbplayers):
        self.__name = name
        self.__nbplayers = nbplayers
    
    @property
    def name(self):
        return self.__name
    
    @property
    def nbplayers(self):
        return self.__nbplayers
    
    @abstractmethod
    def isvalid(self, move):
        ...
    
    def _waitplayers(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 5000))
        s.listen()
        self.__players = []
        while len(self.__players) < self.__nbplayers:
            self.__players.append(s.accept())
    
    def run(self):
        self._waitplayers()