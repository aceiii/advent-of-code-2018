#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


def part1(filename):
    with open(filename) as file:
        twos = 0
        threes = 0
        for line in file:
            letter_counts = {}
            for c in line:
                if c not in letter_counts:
                    letter_counts[c] = 0
                letter_counts[c] += 1
            vals = letter_counts.values()
            if 2 in vals:
                twos += 1
            if 3 in vals:
                threes += 1

        checksum = twos * threes

        print("part1: {0}".format(checksum))


def part2(filename):
    with open(filename) as file:
        lines = file.readlines()
        answer = None
        for i in range(len(lines) - 1):
            line1 = lines[i]
            found = False

            for j in range(i+1, len(lines)):
                line2 = lines[j]
                word = ""
                diff = 0

                for k in range(len(line1)):
                    c1 = line1[k]
                    c2 = line2[k]
                    if c1 != c2:
                        diff += 1
                    else:
                        word += c1

                if diff == 1:
                    answer = word
                    break

            if answer is not None:
                break

        print("part2: {0}".format(answer))


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    main("day2.txt");
