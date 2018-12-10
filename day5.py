#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import string


def part1(filename):
    with open(filename) as file:
        line = file.readline().strip()

        chain = []
        for c in line:
            if len(chain) < 1:
                chain.append(c)
                continue

            prev_c = chain[-1]
            if c.lower() == prev_c.lower() and c != prev_c:
                chain.pop()
            else:
                chain.append(c)

        answer = len(chain)
        print("part1: {}".format(answer))

def part2(filename):
    with open(filename) as file:
        line = file.readline().strip()

        lengths = []
        for c_to_remove in string.lowercase:
            chain = []
            c_upper_to_remove = c_to_remove.upper()
            for c in line:
                if c == c_to_remove or c == c_upper_to_remove:
                    continue

                if len(chain) < 1:
                    chain.append(c)
                    continue

                prev_c = chain[-1]
                if c.lower() == prev_c.lower() and c != prev_c:
                    chain.pop()
                else:
                    chain.append(c)

            lengths.append(len(chain))

        answer = min(lengths)
        print("part2: {}".format(answer))


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    main("day5.txt")
