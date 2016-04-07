#!/usr/bin/env python3
# mirror.py
# author: Sébastien Combéfis
# version: April 8, 2016

import sys

class Mirror:
    def __enter__(self):
        self.__oldwrite = sys.stdout.write
        sys.stdout.write = self._revwrite
        return 'MIROIR'
    
    def _revwrite(self, text):
        self.__oldwrite(text[::-1])
    
    def __exit__(self, type, value, traceback):
        sys.stdout.write = self.__oldwrite

with Mirror() as m:
    print(m)
    print('Hello World!')
print('Normal')