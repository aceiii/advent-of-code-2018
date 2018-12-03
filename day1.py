#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def part1(filename):
    with open(filename, "r") as file:
        ans = 0
        for line in file:
            num = int(line, 10)
            ans += num

        print("part1 answer: {0}".format(ans))


def part2(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        ans = 0
        num = 0
        freq = {}
        index = 0
        N = len(lines)
        while True:
            line = lines[index]
            index = (index + 1) % N

            num += int(line, 10)
            if num not in freq:
                freq[num] = 1
            else:
                freq[num] += 1
            if (freq[num] == 2):
                ans = num
                break

        print("part2 answer: {0}".format(ans))


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    main("day1.txt")
