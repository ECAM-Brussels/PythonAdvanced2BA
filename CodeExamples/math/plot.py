#!/usr/bin/env python3
# plot.py
# author: Sébastien Combéfis
# version: April 5, 2016

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2*np.pi, 2*np.pi, 256, endpoint=True)
y = np.cos(x)

plt.plot(x, y)
plt.show()