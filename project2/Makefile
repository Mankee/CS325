# Project: #2 Dynamic Programming
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
PROGS=prj2

all: $(PROGS)

prj2: dp.o
	$(CC) $(CFLAGS) -o prj2 dp.o main.c

dp.o: dp.c dp.h
	$(CC) $(CFLAGS) -c dp.c

clean:
	rm -f $(PROGS) *.o *~

