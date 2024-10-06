#!/usr/bin/env python

   #Shaktidhar Kanamarla sk10945
   # HW1 - MapReduce -Q2 Reducer Job 2
import sys

def read_mapper_output(file):
    for line in file:
        yield line.strip().split('\t', 1)

def main():
    current_id = 0

    # Sort input in reverse order (highest count first)
    sorted_input = sorted(read_mapper_output(sys.stdin), reverse=True)

    for count, word in sorted_input:
        current_id += 1
        print(f"{current_id}\t{word}")

if __name__ == "__main__":
    main()