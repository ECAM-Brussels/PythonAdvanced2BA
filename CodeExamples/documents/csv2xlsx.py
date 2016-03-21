#!/usr/bin/env python3
# csv2xlsx.py
# author: Sébastien Combéfis
# version: March 21, 2016

import csv
import os.path
import sys

import openpyxl

if __name__ == '__main__' and len(sys.argv) == 2:
    src = sys.argv[1]
    if os.path.exists(src):
        with open(src) as file:
            wb = openpyxl.Workbook()
            sheet = wb.active
            csvreader = csv.reader(file)
            # Go through the CSV file to convert it in XLSs
            row = 1
            for line in csvreader:
                for i in range(len(line)):
                    cell = '{}{}'.format(chr(65 + i), row)
                    sheet[cell] = line[i]
                row += 1
            # Writes the workbook to the disk
            name, ext = os.path.splitext(src)
            dst = '{}.xlsx'.format(name)
            wb.save(dst)