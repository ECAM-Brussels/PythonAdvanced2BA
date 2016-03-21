#!/usr/bin/env python3
# csv2pdf.py
# author: Sébastien Combéfis
# version: March 21, 2016

import csv
import os.path
import sys

import fpdf

if __name__ == '__main__' and len(sys.argv) == 2:
    src = sys.argv[1]
    if os.path.exists(src):
        with open(src) as file:
            doc = fpdf.FPDF()
            doc.add_page()
            csvreader = csv.reader(file)
            # Go through the CSV file to convert it in DOCX
            header_text = next(csvreader)
            epw = doc.w - 2 * doc.l_margin
            col_width = epw / len(header_text)
            # Writes the header
            doc.set_font('Arial', 'B', 10)
            for i in range(len(header_text)):
                doc.cell(col_width, doc.font_size, header_text[i], border=1)
            # Writes the content
            doc.set_font('Arial', '', 10)
            for line in csvreader:
                doc.ln(doc.font_size)
                for elem in line:
                    doc.cell(col_width, doc.font_size, elem, border=1)
            # Writes the document to the disk
            name, ext = os.path.splitext(src)
            dst = '{}.pdf'.format(name)
            doc.output(dst)