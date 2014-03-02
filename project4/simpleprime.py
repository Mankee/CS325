#!/usr/bin/python

import time
import os
import os.path
import shutil

def out(var):
  filename = "prime.txt"
  if os.path.isfile(filename):
    os.rename(filename, "%s.tmp" % filename)
  with open(filename, 'w') as f:
    f.write(str(var) + "\n")



# our worker process.
def find_primes():
  def isprime(start):
    start*=1.0
    for divisor in range(2,int(start**0.5)+1):
      if start/divisor==int(start/divisor): return False
    return True

  check = 2
  while True:
    if isprime(check):
      out(check)
    check += 1

def main():
    find_primes()

main()
