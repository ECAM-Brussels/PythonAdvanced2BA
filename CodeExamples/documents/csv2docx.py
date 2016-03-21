#!/usr/bin/env python3
# csv2docx.py
# author: Sébastien Combéfis
# version: March 21, 2016

import csv
import os.path
import sys

import docx

if __name__ == '__main__' and len(sys.argv) == 2:
    src = sys.argv[1]
    if os.path.exists(src):
        with open(src) as file:
            doc = docx.Document()
            csvreader = csv.reader(file)
            # Go through the CSV file to convert it in DOCX
            header_text = next(csvreader)
            table = doc.add_table(rows=1, cols=len(header_text))
            # Writes the header
            header = table.rows[0].cells
            for i in range(len(header_text)):
                header[i].text = header_text[i]
            # Add the content
            for line in csvreader:
                row = table.add_row().cells
                for i in range(len(line)):
                    row[i].text = line[i]
            # Writes the document to the disk
            name, ext = os.path.splitext(src)
            dst = '{}.docx'.format(name)
            doc.save(dst)