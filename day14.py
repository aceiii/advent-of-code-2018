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
    m = score[i]
    n = score[j]
    o = m + n
    d1 = o // 10
    d2 = o % 10
    if d1 > 0:
        score.append(d1)
    score.append(d2)
    return ((i + m + 1) % len(score), (j + n + 1) % len(score))


def part1(lines):
    N = int(lines[0], 10)
    target = 10
    score = [3, 7]
    elves = (0, 1)
    while len(score) < N + 10:
        elves = step(score, elves)
    return ''.join(str(d) for d in score[N:N+target])


def find(prev_n, score, target):
    n = len(target)
    for i in range(prev_n, len(score) - n):
        if score[i:i+n] == target:
            return i


def part2(lines):
    target = list(map(int, lines[0].strip()))
    n = len(target)
    score = [3,7]
    elves = (0, 1)
    prev_n = 0
    while True:
        elves = step(score, elves)
        if len(score) % 10000 == 0:
            ans = find(prev_n, score, target)
            if ans is not None:
                return ans
            prev_n = len(score) - n - 1


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

