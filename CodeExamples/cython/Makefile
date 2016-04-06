# Makefile
# author: Sébastien Combéfis
# version: April 6, 2016

CC=cc
CFLAGS=-g -O2 -fpic -Wall -I$(PYTHONPATH)/Headers
LDFLAGS=-shared -L$(PYTHONPATH)/lib

all: utils.c lib.pyx
	cython lib.pyx
	$(CC) -c utils.c -o utils.o $(CFLAGS)
	$(CC) -c lib.c -o lib.o $(CFLAGS) `python3-config --cflags`
	$(CC) -shared -o lib.so utils.o lib.o $(LDFLAGS) `python3-config --libs`