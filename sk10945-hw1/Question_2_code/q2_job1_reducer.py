#!/usr/bin/env python

   #Shaktidhar Kanamarla sk10945
   # HW1 - MapReduce -Q2 Mapper Job 2

import sys

def read_mapper_output(file):
    for line in file:
        yield line.strip().split('\t', 1)

def main():
    current_word = None
    current_count = 0

    for word, count in read_mapper_output(sys.stdin):
        try:
            count = int(count)
        except ValueError:
            continue

        if current_word == word:
            current_count += count
        else:
            if current_word:
                print(f"{current_word}\t{current_count}")
            current_word = word
            current_count = count

    if current_word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    main()