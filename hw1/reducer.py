#!/usr/bin/env python

#Shaktidhar Kanamarla sk10945
# HW1 - MapReduce - Reducer

import sys
from collections import defaultdict
from operator import itemgetter

def read_mapper_output(file):
    for line in file:
        yield line.strip().split('\t', 1)

def main():
    word_counts = defaultdict(int)

    # Read the data from standard input
    for word, count in read_mapper_output(sys.stdin):
        word_counts[word] += int(count)

    # Sort the word counts in descending order
    sorted_word_counts = sorted(word_counts.items(), key=itemgetter(1), reverse=True)

    # Output the top 10 words
    for word, count in sorted_word_counts[:10]:
        print(f"{word}\t{count}")

if __name__ == "__main__":
    main()