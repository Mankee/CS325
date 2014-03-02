#!/usr/bin/python

import signal
from sys import exit
import atexit
import time

last_prime = 2

# The signal handler. On receiving sigterm, it writes
# the latest result to the file.
def sig_term(num, frame):
  global last_prime
  with open('last_prime.txt', 'w') as f:
    f.write("largest prime = %s\n" % last_prime)
  print "largest prime = %s" % last_prime

# our worker process.
def find_primes():
  global last_prime
  def isprime(start):
    start*=1.0
    for divisor in range(2,int(start**0.5)+1):
      if start/divisor==int(start/divisor): return False
    return True

  check = 2
  while True:
    if isprime(check):
      last_prime = check
    check += 1

def main():
    # Register signal handler
    signal.signal(signal.SIGTERM, sig_term)
    # do work.
    find_primes()

main()
