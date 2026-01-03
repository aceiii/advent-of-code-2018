#!/usr/bin/env python3

import sys


def parse_lines(lines):
    mode = 0
    initial_state = []
    rules = {}
    for line in lines:
        line = line.strip()
        if line == '':
            mode += 1
            continue
        if mode == 0:
            initial_state = list(line[15:])
        else:
            key, val = line.split(' => ')
            rules[tuple(list(key))] = val
    return initial_state, rules


def get_key(state, idx):
    arr = []
    for i in range(idx-2, idx+3):
        arr.append(state[i] if i in state else '.')
    return tuple(arr)


def apply_rules(state, rules):
    keys = state.keys()
    lo = min(keys)
    hi = max(keys)

    new_state = {}
    for i in range(lo-2, hi+3):
        key = get_key(state, i)
        #print(''.join(key))
        #print(''.join(key) + ' => ' + (rules[key] if key in rules else '.'))
        new_state[i] = rules[key] if key in rules else '.'
    return new_state


def print_state(state):
    keys = state.keys()
    lo = min(keys)
    hi = max(keys)

    line = ['v' if i == 0 else ' ' for i in range(lo, hi+1)]
    print(''.join(line))

    line = []
    for i in range(lo, hi+1):
        v = state[i]
        line.append(state[i] if i in state else '.')
    print(''.join(line))


def plant_values(state):
    return sum([k if v == '#' else 0 for k,v in state.items()])


def part1(lines):
    initial_state, rules = parse_lines(lines)
    state = {i:v for i,v in enumerate(initial_state)}
    n = 20
    #print_state(state)
    val = plant_values(state)
    print(val)
    for _ in range(n):
        state = apply_rules(state, rules)
        #print_state(state)
        new_val = plant_values(state)
        diff = new_val - val
        val = new_val
        print(val, diff)
    return plant_values(state)


def part2(lines):
    target = 50000000000
    initial_state, rules = parse_lines(lines)
    state = {i:v for i,v in enumerate(initial_state)}
    val = plant_values(state)
    diffs = list(range(20))
    while True:
        state = apply_rules(state, rules)
        new_val = plant_values(state)
        diff = new_val - val
        val = new_val
        target -= 1
        if all(d == diff for d in diffs):
            break
        diffs.pop(0)
        diffs.append(diff)
    val += diff * target
    return val


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

