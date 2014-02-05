# Project: #1 MaxSubArray
#
# Team RADZ:
#  Rittie Chuaprasert (chuaprar)
#  Austin Dubina (weila)
#  Darren Baker (bakerdar)
#  Zac Knudson (knudsoza)
# 
# CS 325-400
# Winter 2014
#  
#
#  $RCSfile$
#  $Revision$
#  $Author$
#  $Date$
#  $Log$
#

CC=gcc
DEBUG=-g
CFLAGS=$(DEBUG) -Wall
PROGS=prj1

all: $(PROGS)

prj1: ma.o
	$(CC) $(CFLAGS) -o prj1 ma.o main.c

ma.o: ma.c ma.h
	$(CC) $(CFLAGS) -c ma.c

clean:
	rm -f $(PROGS) *.o *~

