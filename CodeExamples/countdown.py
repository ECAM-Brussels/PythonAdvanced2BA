#!/usr/bin/env python3
# countdown.py
# author: Sébastien Combéfis
# version: February 21, 2016

import sys
import time

counter = 5
while counter > 0:
    print('\b{}'.format(counter), end='')
    sys.stdout.flush()
    counter -= 1
    time.sleep(1)
print('\bBOOM!')