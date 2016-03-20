#!/usr/bin/env python3
# cartprice.py
# author: Sébastien Combéfis
# version: March 20, 2016

import csv
import xml.dom.minidom
import xml.sax

# CSV
src = 'cart.csv'
with open(src, 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    next(csvreader) # Ignore header line
    totalprice = 0
    for line in csvreader:
        totalprice += float(line[3].replace(',', '.'))
    print('Prix total :', totalprice, 'euros')


# XML with SAX
class LibraryHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.__total = 0
    
    @property
    def total(self):
        return self.__total
    
    def startElement(self, tag, attributes):
        if tag == 'book':
            self.__total += float(attributes['price'])
    
    def endElement(self, tag):
        pass
    
    def characters(self, content):
        pass

parser = xml.sax.make_parser()
handler = LibraryHandler()
parser.setContentHandler(handler)

src = 'cart.xml'
parser.parse(src)
print('Prix total :', handler.total, 'euros')


# XML with DOM
src = 'cart.xml'
doc = xml.dom.minidom.parse('cart.xml')
library = doc.documentElement
totalprice = 0
for book in library.getElementsByTagName('book'):
    totalprice += float(book.getAttribute('price'))
print('Prix total :', totalprice, 'euros')