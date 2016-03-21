#!/usr/bin/env python3
# zip.py
# author: Sébastien Combéfis
# version: March 20, 2016

import os.path
import zipfile

# Creates a ZIP archive with one file inside
with zipfile.ZipFile('data.zip', 'w') as file:
    file.write('data.txt')
    file.write('cart.xml')
    file.write('cart.csv')

# Opens the ZIP archive to get information
file = zipfile.ZipFile('data.zip')
file.printdir()
print(file.getinfo('data.txt'))

# Extracts the content of the ZIP archive
file.extractall(os.path.expanduser("~"))