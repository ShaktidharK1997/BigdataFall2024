#!/usr/bin/env python

#Shaktidhar Kanamarla sk10945
# HW1 - MapReduce - Mapper

import sys
import re

# Reading input from the standard input 
# Substituting all non-alphanumeric characters with a space
# Substituting all multiple spaces with a single space
# Splitting the line into words and returning a list of words using a generator
def read_input(source):
    for line in source:
        line = re.sub(r'[^a-zA-Z0-9]', ' ', line)
        line = re.sub(r'\s+', ' ', line)
        yield line.split()

def main():
    data = read_input(sys.stdin)
    for words in data:
        for word in words:
            print('%s\t%s' % (word, 1))


if __name__ == "__main__":
    main()
