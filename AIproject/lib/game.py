# game.py
# Author: Sébastien Combéfis
# Version: March 27, 2016

from abc import *
import copy
import json
import socket

class InvalidMoveException(Exception):
    '''Exception representing an invalid move.'''
    def __init__(self, message):
        super().__init__(message)


class GameState(metaclass=ABCMeta):
    '''Abstract class representing a generic game state.'''
    def __init__(self, initialstate):
        self._state = {'state': initialstate}
    
    def __str__(self):
        return json.dumps(self._state, separators=(',', ':'))
    
    @abstractmethod
    def winner(self):
        '''Check whether the state is a winning state.
        
        Pre: -
        Post: The returned value contains:
              -1 if there is no winner yet (and the game is still going on);
              None if the game ended with a draw;
              the number of the winning player, otherwise.
        '''
        ...
    
    @abstractmethod
    def prettyprint(self):
        '''Print the state.
        
        Pre: -
        Post: This state has been printed on stdout.'''
        ...
    
    @classmethod
    def parse(cls, state):
        return cls(json.loads(state)['state'])


class GameServer(metaclass=ABCMeta):
    '''Abstract class representing a generic game server.'''
    def __init__(self, name, nbplayers, initialstate, verbose=False):
        self.__name = name
        self.__nbplayers = nbplayers
        self.__verbose = verbose
        # Stats about the running game
        self._state = initialstate
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
        '''Apply a move.
    
        Pre: 'move' is valid
        Post: The specified 'move' have been applied to the game for the current player.
        Raises InvalidMoveException: If 'move' is invalid.
        '''
        ...
    
    @property
    def state(self):
        return copy.deepcopy(self._state)
    
    def _waitplayers(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostbyname(socket.gethostname()), 5000))
        s.listen(self.nbplayers)
        if self.__verbose:
            print('Game server listening on {}:{}'.format(socket.gethostbyname(socket.gethostname()), 5000))
        self.__players = []
        # Wait for enough players for a play
        while len(self.__players) < self.__nbplayers:
            self.__players.append(s.accept()[0])
            if self.__verbose:
                print('New client connected', len(self.__players), '/', self.nbplayers)
        # Notify players that the game started
        try:
            for player in self.__players:
                player.sendall('START'.encode())
                data = player.recv(1024).decode()
                if data != 'READY':
                    return False
        except OSError:
            if self.__verbose:
                print('Error while notifying player {}'.format(player))
            return False
        return True
        if self.__verbose:
            print('Game started')

    def _gameloop(self):
        self.__currentplayer = 0
        winner = -1
        while winner == -1:
            player = self.__players[self.__currentplayer]
            if self.__verbose:
                print('Player', self.__currentplayer, "'s turn")
            player.sendall('PLAY {}'.format(self.state).encode())
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
                player.sendall('ERROR {}'.format(e).encode())
            if self.__verbose:
                print('State of the game:')
                self._state.prettyprint()
            winner = self._state.winner()
        # Notify players about won/lost status
        if winner != None:
            for i in range(self.nbplayers):
                self.__players[i].sendall(('WON' if winner == i else 'LOST').encode())
            if self.__verbose:
                print('The winner is player', winner)
        # Notify players that the game ended
        else:
            for player in self.__players:
                player.sendall('END'.encode())
        # Close the connexions with the clients
        for player in self.__players:
            player.close()
        if self.__verbose:
            print('Game ended')
    
    def run(self):
        if self._waitplayers():
            self._gameloop()
        elif self.__verbose:
            print('Players not ready')


class GameClient(metaclass=ABCMeta):
    '''Abstract class representing a game client'''
    def __init__(self, server, stateclass, verbose=False):
        self.__stateclass = stateclass
        self.__verbose = verbose
        addrinfos = socket.getaddrinfo(*server, socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        try:
            s.connect(addrinfos[0][4])
            if self.__verbose:
                print('Connected to the game server on {}:{}'.format(*addrinfos[0][4]))
            self.__server = s
            self._gameloop()
        except OSError:
            print('Impossible to connect to the game server on {}:{}'.format(*addrinfos[0][4]))
    
    def _gameloop(self):
        server = self.__server
        running = True
        while running:
            data = server.recv(1024).decode()
            command = data[:data.index(' ')] if ' ' in data else data
            if command == 'START':
                server.sendall('READY'.encode())
                if self.__verbose:
                    print('Game started')
            elif command == 'PLAY':
                state = self.__stateclass.parse(data[data.index(' ')+1:])
                if self.__verbose:
                    print("Player's turn to play")
                    print('State of the game:')
                    state.prettyprint()
                move = self._nextmove(state)
                if self.__verbose:
                    print('Next move:', move)
                server.sendall(move.encode())
            elif command in ('WON', 'LOST', 'END'):
                running = False
                if self.__verbose:
                    if command == 'WON':
                        print('You won the game')
                    elif command == 'LOST':
                        print('You lost the game')
                    else:
                        print('Game ended')
                server.close()
            else:
                if self.__verbose:
                    print('Specific data received:', data)
                self._handle(data)
    
    @abstractmethod
    def _handle(self, command):
        '''Handle a command.
        
        Pre: command != ''
        Post: The specified 'command' has been handled.
        '''
        ...
    
    @abstractmethod
    def _nextmove(self, state):
        '''Get the next move to play.
        
        Pre: 'state' is a valid game' state.
        Post: The returned value contains a valid move to be played by this player
              in the specified 'state' of the game.
        '''
        ...