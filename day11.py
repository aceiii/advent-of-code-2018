#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function


power_level_cache = {}
def power_level(x, y, serial_number):
    key = (x, y, serial_number)

    if key in power_level_cache:
        return power_level_cache[key]

    rack_id = x + 10
    power = rack_id * y
    power += serial_number
    power *= rack_id
    power = (power / 100) % 10 if power > 100 else 0
    return int(power - 5)


def part1(serial_number):
    serial_number = 18
    N = 300
    grid = [[0] * N for _ in range(N)]
    max_power = (0, (0, 0))

    for y in range(N):
        for x in range(N):
            p = sum([power_level(x + i, y + j, serial_number) for j in range(1, 4) for i in range(1, 4)])
            grid[y][x] = p
            if p > max_power[0]:
                max_power = (p, (x, y))

    p, (x, y) = max_power
    print(f"part1: {x+1},{y+1}")


def part2(serial_number):
    max_powers = []

    def solve(n):
        N = 300
        grid = [[0] * N for _ in range(N-(n-1))]
        max_power = (0, (0, 0))

        for y in range(N-(n-1)):
            for x in range(N-(n-1)):
                p = sum([power_level(x + i, y + j, serial_number) for j in range(1, n+1) for i in range(1, n+1)])
                grid[y][x] = p
                if p > max_power[0] or (x == 0 and y == 0):
                    max_power = (p, (x, y))

        p, (x, y) = max_power
        return p, n, (x, y)

    for n in range(1, 301):
        max_powers.append(solve(n))

    max_powers.sort()
    _, n, (x, y) = max_powers[0]

    print(f"part2: {x},{y},{n}")


def main(serial_number):
    part1(serial_number)
    part2(serial_number)


if __name__ == "__main__":
    main(5468)
