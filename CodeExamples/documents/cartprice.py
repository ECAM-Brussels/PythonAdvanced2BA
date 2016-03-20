#!/usr/bin/env python3
# cartprice.py
# author: Sébastien Combéfis
# version: March 20, 2016

import csv

src = 'cart.csv'
with open(src, 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    next(csvreader) # Ignore header line
    totalprice = 0
    for line in csvreader:
        totalprice += float(line[3].replace(',', '.'))
    print('Prix total :', totalprice, 'euros')