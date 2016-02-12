# game.py
# Author: Sébastien Combéfis
# Version: February 12, 2016

from abc import *
import socket

class InvalidMoveException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GameServer(metaclass=ABCMeta):
    def __init__(self, name, nbplayers):
        self.__name = name
        self.__nbplayers = nbplayers
        self.__currentplayer = None
        self.__turns = 0
    
    @property
    def name(self):
        return self.__name
    
    @property
    def nbplayers(self):
        return self.__nbplayers
    
    @property
    def currentplayer(self):
        return self.__currentplayer
    
    @property
    def turns(self):
        return self.__turns
    
    @abstractmethod
    def applymove(self, move):
        ...
    
    @abstractmethod
    def isfinished(self):
        ...
    
    def _waitplayers(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 5000))
        s.listen()
        self.__players = []
        while len(self.__players) < self.__nbplayers:
            self.__players.append(s.accept())
    
    def _gameloop(self):
        self.__currentplayer = 0
        while not self.isfinished():
            self.__turns += 1
            self.__currentplayer = (self.__currentplayer + 1) % self.nbplayers
    
    def run(self):
        self._waitplayers()
        self._gameloop()


class GameClient(metaclass=ABCMeta):
    def __init__(self, server):
        self.__server = socket.getaddrinfo(*server, socket.AF_INET, socket.SOCK_STREAM)[0][4]
        s = socket.socket()
        s.connect(self.__server)