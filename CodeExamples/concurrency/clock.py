#!/usr/bin/env python3
# clock.py
# author: Sébastien Combéfis
# version: March 6, 2016

import sched
from datetime import datetime
import sys
import time

def printhour():
    print('\r{0:%H:%M:%S}'.format(datetime.now()), end='')
    sys.stdout.flush()
    scheduler.enter(1, 1, printhour)

scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(1, 1, printhour)
try:
    scheduler.run()
except KeyboardInterrupt:
    print()