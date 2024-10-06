#!/usr/bin/env python

   #Shaktidhar Kanamarla sk10945
   # HW1 - MapReduce -Q2 Mapper Job 1

import sys
import re

def read_input(source):
    for line in source:
        # Replace multiple spaces with a single space
        line = re.sub(r'\s+', ' ', line.strip())
        # Split on whitespace and keep special characters as separate tokens
        tokens = re.findall(r'\w+|[!-/:-@[-`{-~]', line)
        if len(tokens) >= 1:  # Ignore lines with less than 1 word
            yield tokens

def main():
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            print('%s\t%s' % (word, 1))

if __name__ == "__main__":
    main()