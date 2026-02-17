#!/usr/bin/env python3

import sys


def parse_samples(lines):
    before = [int(a, 10) for a in lines[0][9:-1].split(',')]
    op= [int(a, 10) for a in lines[1].split(' ')]
    after = [int(a, 10) for a in lines[2][9:-1].split(',')]
    return { "op": op, "before": before, "after": after }


def parse_instrs(line):
    return [int(a, 10) for a in line.split(' ')]


def parse(lines):
    prev = []
    samples = []
    instrs = []
    blank = 0
    mode = 0
    for idx,line in enumerate(lines):
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
                mode = 1
                blank = 0
        else:
            instrs.append(line.strip())
    return [parse_samples(i) for i in samples], [parse_instrs(i) for i in instrs]


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
    samples, _ = parse(lines)
    answer = 0
    for sample in samples:
        if test_sample(sample) >= 3:
            answer += 1
    return answer


def solve_ops(samples):
    ops_map = {k:[1] * 16 for k in range(16)}
    for sample in samples:
        for idx, op_func in enumerate(all_ops):
            regs = sample["before"][:]
            op_id, a, b, c = sample["op"]
            op_func(regs, a, b, c)
            if regs != sample["after"]:
                ops_map[op_id][idx] = 0

    ops = list(ops_map.items())
    known_ops = {}
    used_ops = set()

    while ops:
        ops.sort(key=lambda a: sum(a[1]), reverse=True)
        while ops and sum(ops[-1][1]) == 1:
            k,v = ops.pop()
            op_idx = v.index(1)
            known_ops[k] = op_idx
            used_ops.add(op_idx)
        for op in ops:
            for i in range(16):
                if i in used_ops:
                    op[1][i] = 0
    return known_ops


def run(regs, ops, instrs):
    for op_id, a, b, c in instrs:
        op_func = all_ops[ops[op_id]]
        op_func(regs, a, b, c)


def part2(lines):
    samples, instrs = parse(lines)
    ops = solve_ops(samples)
    regs = [0, 0, 0, 0]
    run(regs, ops, instrs)
    return regs[0]


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

