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
            self.__players.append(s.accept()[0])
        for player in self.__players:
            player.send('START'.encode())
    
    def _gameloop(self):
        self.__currentplayer = 0
        while not self.isfinished():
            player = self.__players[self.__currentplayer]
            player.send('PLAY'.encode())
            try:
                self.applymove(player.recv(1024))
                self.__turns += 1
                self.__currentplayer = (self.__currentplayer + 1) % self.nbplayers
            except InvalidMoveException as e:
                player.send('ERROR {}'.format(e))
    
    def run(self):
        self._waitplayers()
        self._gameloop()


class GameClient(metaclass=ABCMeta):
    def __init__(self, server):
        addrinfos = socket.getaddrinfo(*server, socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        s.connect(addrinfos[0][4])
        self.__server = s
        self._gameloop()
    
    def _gameloop(self):
        server = self.__server
        running = True
        while running:
            command = server.recv(1024).decode()
            if command == 'START':
                print('Game started')
            else:
                self._handlecommand(command)
            command = ''
    
    @abstractmethod
    def _handlecommand(self, command):
        ...