#!/usr/bin/env python3
# adder.py
# author: Sébastien Combéfis
# version: February 14, 2016

import pickle
import socket
import struct
import sys

SERVERADDRESS = (socket.gethostname(), 6000)

class AdderServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            self._handle(client)
            client.close()
    
    def _handle(self, client):
        size = struct.unpack('I', client.recv(4))[0]
        data = pickle.loads(client.recv(size))
        result = sum(data)
        print('Somme de {} = {}'.format(data, result))
        client.send(struct.pack('I', result))


class AdderClient():
    def __init__(self, message):
        self.__data = [int(x) for x in message]
        self.__s = socket.socket()
    
    def run(self):
        self.__s.connect(SERVERADDRESS)
        print('Somme:', self._compute())
        self.__s.close()
    
    def _compute(self):
        totalsent = 0
        msg = pickle.dumps(self.__data)
        self.__s.send(struct.pack('I', len(msg)))
        while totalsent < len(msg):
            sent = self.__s.send(msg[totalsent:])
            totalsent += sent
        return struct.unpack('I', self.__s.recv(4))[0]

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        AdderServer().run()
    elif len(sys.argv) > 2 and sys.argv[1] == 'client':
        AdderClient(sys.argv[2:]).run()