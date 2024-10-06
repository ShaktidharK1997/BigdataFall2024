#!/usr/bin/env python

#Shaktidhar Kanamarla sk10945
# HW1 - MapReduce - Reducer Job 2
import sys
import heapq

def read_mapper_output(file):
    for line in file:
        yield line.strip().split('\t', 1)

def main():
    heap = []
    for word, count in read_mapper_output(sys.stdin):
        count = int(count)
        if len(heap) < 10:
            heapq.heappush(heap, (count, word))
        else:
            heapq.heappushpop(heap, (count, word))

    # Output the final top 10 words
    for count, word in sorted(heap, reverse=True):
        print(f"{word}\t{count}")

if __name__ == "__main__":
    main()