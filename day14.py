#!/usr/bin/env python3

import sys


def parse_score(line):
    score = []
    for c in line.strip():
        n = int(c, 10)
        score.append(n)
    return score


def step(score, elves):
    i, j = elves
    new_score = score[:]
    i2 = new_score[i]
    j2 = new_score[j]
    for c in str(i2 + j2):
        new_score.append(int(c, 10))
    return new_score, ((i + i2 + 1) % len(new_score), (j + j2 + 1) % len(new_score))

def part1(lines):
    N = int(lines[0], 10)
    target = 10
    score = [3, 7]
    elves = (0, 1)
    while len(score) < N + 10:
        score, elves = step(score, elves)
    return ''.join(str(d) for d in score[N:N+target])


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

