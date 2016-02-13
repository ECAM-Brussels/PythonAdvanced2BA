#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 13, 2016

import sys

class EchoServer():
    def run(self):
        print('Run server')


class EchoClient():
    def __init__(self, message):
        self.__message = message
    
    def run(self):
        print('Run client', self.__message)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2]).run()