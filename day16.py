#!/usr/bin/env python3

import sys


def parse_samples(lines):
    before = [int(a, 10) for a in lines[0][9:-1].split(',')]
    op= [int(a, 10) for a in lines[1].split(' ')]
    after = [int(a, 10) for a in lines[2][9:-1].split(',')]
    return { "op": op, "before": before, "after": after }


def parse(lines):
    prev = []
    samples = []
    test = []
    blank = 0
    mode = 0
    for line in lines:
        if mode == 0:
            if line.strip() == '':
                blank += 1
            else:
                blank = 0
                prev.append(line.strip())

            if blank == 1:
                samples.append(prev)
                prev = []
            elif blank == 3:
                mode == 1
                blank = 0
                continue
        else:
            samples.append(line.strip())
    return [parse_samples(i) for i in samples], test


def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]

def addi(regs, a, b, c):
    regs[c] = regs[a] + b

def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]

def muli(regs, a, b, c):
    regs[c] = regs[a] * b

def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]

def bani(regs, a, b, c):
    regs[c] = regs[a] & b

def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]

def bori(regs, a, b, c):
    regs[c] = regs[a] | b

def setr(regs, a, b, c):
    regs[c] = regs[a]

def seti(regs, a, b, c):
    regs[c] = a

def gtir(regs, a, b, c):
    regs[c] = 1 if a > regs[b] else 0

def gtri(regs, a, b, c):
    regs[c] = 1 if regs[a] > b else 0

def gtrr(regs, a, b, c):
    regs[c] = 1 if regs[a] > regs[b] else 0

def eqir(regs, a, b, c):
    regs[c] = 1 if a == regs[b] else 0

def eqri(regs, a, b, c):
    regs[c] = 1 if regs[a] == b else 0

def eqrr(regs, a, b, c):
    regs[c] = 1 if regs[a] == regs[b] else 0



all_ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def test_sample(sample):
    n = 0
    for op_func in all_ops:
        regs = sample["before"][:]
        _, a, b, c = sample["op"]
        op_func(regs, a, b, c)
        if regs == sample["after"]:
            n += 1
    return n


def part1(lines):
    samples, test = parse(lines)
    answer = 0
    for sample in samples:
        if test_sample(sample) >= 3:
            answer += 1
    return answer


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

