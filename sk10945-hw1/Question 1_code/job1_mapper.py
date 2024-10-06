#!/usr/bin/env python

   #Shaktidhar Kanamarla sk10945
   # HW1 - MapReduce - Mapper Job 1

import sys
import re

import sys
import re

def read_input(source):
    for line in source:
        # Replace multiple spaces with a single space
        line = re.sub(r'\s+', ' ', line.strip())
        # Split on whitespace and keep punctuation as separate tokens
        tokens = re.findall(r'\w+|[^\w\s]', line)
        if len(tokens) >= 1:  # Ignore lines with less than 1 word
            yield tokens

def main():
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            print('%s\t%s' % (word, 1))

if __name__ == "__main__":
    main()