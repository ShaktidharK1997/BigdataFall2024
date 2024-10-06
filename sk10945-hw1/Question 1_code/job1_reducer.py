#!/usr/bin/env python

#Shaktidhar Kanamarla sk10945
# HW1 - MapReduce - Reducer Job 1

import sys
import heapq

def read_mapper_output(file):
    for line in file:
        yield line.strip().split('\t', 1)

def main():
    word_counts = {}
    top_k = 100  # Adjust this value based on your data size and memory constraints

    for word, count in read_mapper_output(sys.stdin):
        try:
            count = int(count)
        except ValueError:
            continue

        if word in word_counts:
            word_counts[word] += count
        else:
            word_counts[word] = count

    # Use a min-heap to keep the top K words
    heap = []
    for word, count in word_counts.items():
        if len(heap) < top_k:
            heapq.heappush(heap, (count, word))
        else:
            heapq.heappushpop(heap, (count, word))

    # Output the top K words
    for count, word in sorted(heap, reverse=True):
        print(f"{word}\t{count}")

if __name__ == "__main__":
    main()