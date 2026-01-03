#!/usr/bin/env python3

import sys


DIRS = {'<': (-1,0), 'v': (0,1), '>': (1,0), '^': (0,-1)}
TURNS = [
            { '<': 'v', '^': '<', '>': '^', 'v': '>' },
            { '<': '<', '^': '^', '>': '>', 'v': 'v' },
            { '<': '^', '^': '>', '>': 'v', 'v': '<' },
        ]
TILE = {
        '-': { '<': '<', '>': '>' },
        '|': { '^': '^', 'v': 'v' },
        '/': { '^': '>', '<': 'v', '>': '^', 'v': '<' },
        '\\': { '^': '<', '>': 'v', 'v': '>', '<': '^' },
        }
OPPOSITE = {'<':'>', '>':'<', '^':'v', 'v':'^'}


def parse(lines):
    grid = {}
    carts = []
    height = len(lines)
    width = len(lines[0])
    dims = width, height
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            pos = (x,y)
            if c in '<v^>':
                carts.append((pos, c, 0))
                if c == '<' or c == '>':
                    grid[pos] = '-'
                else:
                    grid[pos] = '|'
            elif c != ' ':
                grid[pos] = c
    return grid, dims, carts


def draw_grid(grid, dims, carts=[], crash=None):
    grid = grid.copy()
    if crash:
        grid[crash] = 'X'
    else:
        for pos,c,_ in carts:
            grid[pos] = c
    print()
    width, height = dims
    for y in range(height):
        line = []
        for x in range(width):
            pos = (x,y)
            line.append(grid[pos] if pos in grid else ' ')
        print(''.join(line))
    print()


def tick(grid, dims, carts):
    new_carts = []

    old_pos = set()
    for pos, c, _ in carts:
        old_pos.add((pos, OPPOSITE[c]))

    cart_pos = set()
    crash = None

    for pos, c, t in carts:
        x, y = pos
        dx, dy = DIRS[c]
        nx, ny = x + dx, y + dy
        pos = nx, ny
        if pos in cart_pos or (pos,c) in old_pos:
            return carts, pos

        tile = grid[pos]
        if tile == '+':
            c = TURNS[t][c]
            t = (t + 1) % len(TURNS)
        else:
            c = TILE[tile][c]
        cart_pos.add(pos)
        new_carts.append((pos, c, t))

    return new_carts, crash

def part1(lines):
    grid, dims, carts = parse(lines)
    i = 0
    while True:
        carts, crash = tick(grid, dims, carts)
        #draw_grid(grid, dims, carts, crash)
        if crash:
            return crash


def part2(lines):
    pass


def main():
    lines = sys.stdin.read().strip().split("\n")
    print("Part1: {}".format(part1(lines)))
    print("Part2: {}".format(part2(lines)))


if __name__ == "__main__":
    main()

