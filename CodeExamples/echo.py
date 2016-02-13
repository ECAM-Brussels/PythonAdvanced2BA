#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 13, 2016

import socket
import sys

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        
    def run(self):
        print('Run server')
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            print(client.recv(1024).decode())


class EchoClient():
    def __init__(self, message):
        self.__message = message
        self.__s = socket.socket()
    
    def run(self):
        print('Run client')
        self.__s.connect(SERVERADDRESS)
        self.__s.send(self.__message)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2].encode()).run()