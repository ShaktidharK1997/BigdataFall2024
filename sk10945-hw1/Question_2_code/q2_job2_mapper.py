#!/usr/bin/env python

   #Shaktidhar Kanamarla sk10945
   # HW1 - MapReduce -Q2 Mapper Job 2

import sys

def main():
    for line in sys.stdin:
        word, count = line.strip().split('\t')
        # Emit count as key and word as value
        print(f"{int(count):010d}\t{word}")

if __name__ == "__main__":
    main()