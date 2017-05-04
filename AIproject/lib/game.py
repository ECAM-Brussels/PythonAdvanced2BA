# game.py
# Author: Sébastien Combéfis
# Version: April 20, 2016

from abc import *
import copy
import json
import socket
import sys

DEFAULT_BUFFER_SIZE = 1024
SECTION_WIDTH = 60


def _printsection(title):
    print()
    print(' {} '.format(title).center(SECTION_WIDTH, '='))


class InvalidMoveException(Exception):
    '''Exception representing an invalid move.'''
    def __init__(self, message):
        super().__init__(message)


class GameState(metaclass=ABCMeta):
    '''Abstract class representing a generic game state.'''
    def __init__(self, visible, hidden=None):
        self._state = {'visible': visible, 'hidden': hidden}

    def __str__(self):
        return json.dumps(self._state['visible'], separators=(',', ':'))

    def __repr__(self):
        return json.dumps(self._state, separators=(',', ':'))

    @abstractmethod
    def winner(self):
        '''Check whether the state is a winning state.

        Pre: -
        Post: The returned value contains:
              -1 if there is no winner yet (and the game is still going on);
              None if the game ended with a draw;
              or the number of the winning player, otherwise.
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
        return cls(json.loads(state))

    @classmethod
    def buffersize(cls):
        return DEFAULT_BUFFER_SIZE


class GameServer(metaclass=ABCMeta):
    '''Abstract class representing a generic game server.'''
    def __init__(self, name, nbplayers, initialstate, verbose=False):
        self.__name = name
        self.__nbplayers = nbplayers
        self.__verbose = verbose
        self._state = initialstate
        # Stats about the running game
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
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 5000))
        s.listen(self.nbplayers)
        if self.__verbose:
            _printsection('Starting {}'.format(self.name))
            try:
                print(' Game server listening on {}:{}.'.format(socket.gethostbyname(socket.gethostname()), 5000))
            except:
                print(' Game server listening on port {}.'.format(5000))
            print(' Waiting for {} players...'.format(self.nbplayers))
        self.__players = []
        # Wait for enough players for a play
        try:
            while len(self.__players) < self.__nbplayers:
                client = s.accept()[0]
                self.__players.append(client)
                if self.__verbose:
                    print(' - Client connected from {}:{} ({}/{}).'
                          .format(*client.getpeername(), len(self.__players), self.nbplayers)
                          )
        except KeyboardInterrupt:
            for player in self.__players:
                player.close()
            _printsection('Game server ended')
            return False
        # Notify players that the game started
        try:
            for i in range(len(self.__players)):
                if self.__verbose:
                    print(' Initialising player {}...'.format(i))
                player = self.__players[i]
                player.sendall('START {}'.format(i).encode())
                data = player.recv(self._state.__class__.buffersize()).decode().split(' ')
                if data[0] != 'READY':
                    if self.__verbose:
                        print(' - Player {} not ready to start.'.format(i))
                        _printsection('Current game ended')
                    return False
                elif self.__verbose:
                    print(' - Player {} ({}) ready to start.'.format(i, data[1] if len(data) == 2 else 'Anonymous'))
        except OSError:
            if self.__verbose:
                print('Error while notifying player {}.'.format(player))
            return False
        # Start the game since all the players are ready
        if self.__verbose:
            _printsection('Game initialised (all players ready to start)')
        return True

    def _gameloop(self):
        self.__currentplayer = 0
        winner = -1
        if self.__verbose:
            print(' Initial state:')
            self._state.prettyprint()
        # Loop until the game ends with a winner or with a draw
        while winner == -1:
            player = self.__players[self.__currentplayer]
            if self.__verbose:
                print("\n=> Turn #{} (player {})".format(self.turns, self.__currentplayer))
            player.sendall('PLAY {}'.format(self.state).encode())
            try:
                move = player.recv(self._state.__class__.buffersize()).decode()
                if self.__verbose:
                    print('   Move:', move)
                self.applymove(move)
                self.__turns += 1
                self.__currentplayer = (self.__currentplayer + 1) % self.nbplayers
            except InvalidMoveException as e:
                if self.__verbose:
                    print('Invalid move:', e)
                player.sendall('ERROR {}'.format(e).encode())
            if self.__verbose:
                print('   State:')
                self._state.prettyprint()
            winner = self._state.winner()
        if self.__verbose:
            _printsection('Game finished')
        # Notify players about won/lost status
        if winner is not None:
            for i in range(self.nbplayers):
                self.__players[i].sendall(('WON' if winner == i else 'LOST').encode())
            if self.__verbose:
                print(' The winner is player {}.'.format(winner))
        # Notify players that the game ended
        else:
            for player in self.__players:
                player.sendall('END'.encode())
        # Close the connexions with the clients
        for player in self.__players:
            player.close()
        if self.__verbose:
            _printsection('Game ended')

    def run(self):
        if self._waitplayers():
            self._gameloop()


class GameClient(metaclass=ABCMeta):
    '''Abstract class representing a game client'''
    def __init__(self, server, stateclass, verbose=False):
        self.__stateclass = stateclass
        self.__verbose = verbose
        if self.__verbose:
            _printsection('Starting game')
        addrinfos = socket.getaddrinfo(*server, socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        try:
            s.connect(addrinfos[0][4])
            if self.__verbose:
                print(' Connected to the game server on {}:{}.'.format(*addrinfos[0][4]))
            self.__server = s
            self._gameloop()
        except OSError:
            print(' Impossible to connect to the game server on {}:{}.'.format(*addrinfos[0][4]))

    def _gameloop(self):
        server = self.__server
        running = True
        while running:
            data = server.recv(self.__stateclass.buffersize()).decode()
            command = data[:data.index(' ')] if ' ' in data else data
            if command == 'START':
                self._playernb = int(data[data.index(' '):])
                server.sendall('READY'.encode())
                if self.__verbose:
                    _printsection('Game started')
                    print("   Player's number: {}".format(self._playernb))
            elif command == 'PLAY':
                state = self.__stateclass.parse(data[data.index(' ')+1:])
                if self.__verbose:
                    print("\n=> Player's turn to play")
                    print('   State:')
                    state.prettyprint()
                move = self._nextmove(state)
                if self.__verbose:
                    print('   Move:', move)
                server.sendall(move.encode())
            elif command in ('WON', 'LOST', 'END'):
                running = False
                if self.__verbose:
                    _printsection('Game finished')
                    if command == 'WON':
                        print(' You won the game.')
                    elif command == 'LOST':
                        print(' You lost the game.')
                    else:
                        print(' It is draw.')
                    _printsection('Game ended')
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
