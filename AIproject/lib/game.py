# game.py
# Author: Sébastien Combéfis
# Version: February 12, 2016

from abc import *
import socket

class InvalidMoveException(Exception):
    def __init__(self, message):
        super().__init__(message)


class GameServer(metaclass=ABCMeta):
    def __init__(self, name, nbplayers, verbose=False):
        self.__name = name
        self.__nbplayers = nbplayers
        self.__verbose = verbose
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
    
    @property
    @abstractmethod
    def state(self):
        ...
    
    def _waitplayers(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), 5000))
        s.listen()
        self.__players = []
        # Wait for enough players for a play
        while len(self.__players) < self.__nbplayers:
            self.__players.append(s.accept()[0])
            if self.__verbose:
                print('New client connected', len(self.__players), '/', self.nbplayers)
        # Notify players that the game started
        for player in self.__players:
            player.send('START'.encode())
        if self.__verbose:
            print('Game started')
    
    def _gameloop(self):
        self.__currentplayer = 0
        while not self.isfinished():
            player = self.__players[self.__currentplayer]
            if self.__verbose:
                print('Player', self.__currentplayer, "'s turn")
                print('State of the game:', self.state)
            player.send('PLAY {}'.format(self.state).encode())
            try:
                move = player.recv(1024).decode()
                if self.__verbose:
                    print('Move:', move)
                self.applymove(move)
                self.__turns += 1
                self.__currentplayer = (self.__currentplayer + 1) % self.nbplayers
            except InvalidMoveException as e:
                if self.__verbose:
                    print('Invalid move:', e)
                player.send('ERROR {}'.format(e).encode())
    
    def run(self):
        self._waitplayers()
        self._gameloop()


class GameClient(metaclass=ABCMeta):
    def __init__(self, server, verbose=False):
        self.__verbose = verbose
        addrinfos = socket.getaddrinfo(*server, socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        s.connect(addrinfos[0][4])
        if self.__verbose:
            print('Connected to the server')
        self.__server = s
        self._gameloop()
    
    def _gameloop(self):
        server = self.__server
        running = True
        while running:
            data = server.recv(1024).decode()
            command = data[:data.index(' ')] if ' ' in data else data
            if command == 'START':
                if self.__verbose:
                    print('Game started')
            elif command == 'PLAY':
                state = data[data.index(' ')+1:]
                if self.__verbose:
                    print("Player's turn to play")
                    print('State of the game:', state)
                move = self._nextmove(state)
                if self.__verbose:
                    print('Next move:', move)
                server.send(move.encode())
            else:
                if self.__verbose:
                    print('Specific data received:', data)
                self._handle(data)
    
    @abstractmethod
    def _handle(self, command):
        ...
    
    @abstractmethod
    def _nextmove(self, state):
        ...