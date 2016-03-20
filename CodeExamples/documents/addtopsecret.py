#!/usr/bin/env python3
# addtopsecret.py
# author: Sébastien Combéfis
# version: March 20, 2016

import os.path
import sys

import PyPDF2

if __name__ == '__main__' and len(sys.argv) == 2:
    src = sys.argv[1]
    if os.path.exists(src):
        # Adds a 'Top Secret' watermark to all the pages
        with open(src, 'rb') as file1, open('topsecret.pdf', 'rb') as file2:
            pdfreader = PyPDF2.PdfFileReader(file1)
            pdfwriter = PyPDF2.PdfFileWriter()
            for i in range(pdfreader.numPages):
                watermark = PyPDF2.PdfFileReader(file2).getPage(0)
                page = pdfreader.getPage(i)
                watermark.mergePage(page)
                pdfwriter.addPage(watermark)
            # Writes the result file
            name, ext = os.path.splitext(src)
            dst = os.path.join(os.path.dirname(src), '{}_secret.{}'.format(name, ext))
            with open(dst, 'wb') as output:
                pdfwriter.write(output)