#!/usr/bin/env python3
# adder.py
# author: Sébastien Combéfis
# version: February 15, 2016

import pickle
import socket
import struct
import sys

PORT = 6000

class AdderServer:
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(("0.0.0.0", PORT))
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                self._handle(client)
                client.close()
            except OSError:
                print('Erreur lors du traitement de la requête du client.')
    
    def _handle(self, client):
        size = struct.unpack('I', client.recv(4))[0]
        data = pickle.loads(client.recv(size))
        result = sum(data)
        print('Somme de {} = {}'.format(data, result))
        client.send(struct.pack('I', result))


class AdderClient:
    def __init__(self, message, serverIP="127.0.0.1"):
        self.__data = [int(x) for x in message]
        self.__s = socket.socket()
        self.serverIP = serverIP
    
    def run(self):
        try:
            self.__s.connect((self.serverIP, PORT))
            print('Somme:', self._compute())
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
    
    def _compute(self):
        try:
            totalsent = 0
            msg = pickle.dumps(self.__data)
            self.__s.send(struct.pack('I', len(msg)))
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
            return struct.unpack('I', self.__s.recv(4))[0]
        except OSError:
            print("Erreur lors du calcul de la somme.")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        AdderServer().run()
    
    elif len(sys.argv) > 2 and sys.argv[1] == 'client':
        params = sys.argv[2:]

        try:
            isInt = int(params[0])
            AdderClient(params).run()
        except:
            ip = params[0]
            params = params[1:]
            AdderClient(params, ip).run()