#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016

import socket
import sys

PORT = 6000

class EchoServer:
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(("0.0.0.0", PORT))
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                print(self._receive(client).decode())
                client.close()
            except OSError:
                print('Erreur lors de la réception du message.')
    
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)


class EchoClient:
    def __init__(self, message, serverIP="127.0.0.1"):
        self.__message = message
        self.__s = socket.socket()
        self.serverIP = serverIP
    
    def run(self):
        try:
            self.__s.connect((self.serverIP, PORT))
            self._send()
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
    
    def _send(self):
        totalsent = 0
        msg = self.__message
        try:
            while totalsent < len(msg):
                sent = self.__s.send(msg[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    elif len(sys.argv) > 2 and sys.argv[1] == 'client':
        if len(sys.argv) == 3:
            EchoClient(sys.argv[2].encode()).run()
        else:
            EchoClient(sys.argv[3].encode(), sys.argv[2]).run()