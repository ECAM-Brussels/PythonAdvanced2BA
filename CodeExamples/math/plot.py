#!/usr/bin/env python3
# plot.py
# author: Sébastien Combéfis
# version: April 5, 2016

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-2*np.pi, 2*np.pi, 256, endpoint=True)
c = np.cos(x)
s = np.sin(x)

plt.plot(x, c, linewidth=2.5, label='cos(x)')
plt.plot(x, s, color='red', label='sin(x)')

plt.ylim(-2, 2)
plt.xticks(
    [-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    [r'$-2\pi$', r'$\pi$', '0', r'$\pi$', r'$2\pi$']
)
plt.legend(loc='upper right')
plt.show()