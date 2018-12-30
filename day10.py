#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re


class Point(object):
    def __init__(self, x, y, vx, vy):
        self.pos = (x, y)
        self.vel = (vx, vy)

    def __repr__(self):
        return "Point({},{})".format(self.pos, self.vel)

    def update(self):
        x, y = self.pos
        vx, vy = self.vel
        self.pos = (x + vx, y + vy)


def part1(filename):
    points = []
    with open(filename) as file:
        for line in file:
            pattern = r"^position=\< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>$"
            match = re.match(pattern, line)
            x, y, vx, vy = map(int, match.groups())
            points.append(Point(x, y, vx, vy))

    N = 100000
    m = (-float("inf"), 0, None, None)

    for i in range(N):
        filled_pos = {}
        adj_count = 0
        ps = []
        min_x = float("inf")
        min_y = float("inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for p in points:
            p.update()
            filled_pos[p.pos] = True
            ps.append(p.pos)

        for p in points:
            x, y = p.pos

            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y

            left = (x - 1, y)
            right = (x + 1, y)
            top  = (x, y - 1)
            bottom = (x, y + 1)

            if (left in filled_pos or
                right in filled_pos or
                top in filled_pos or
                bottom in filled_pos):
                    adj_count += 1

        if adj_count > m[0]:
            m = (adj_count, i + 1, filled_pos, (min_x, min_y, max_x, max_y))

    min_x, min_y, max_x, max_y = m[3]
    w = max_x - min_x + 1
    h = max_y - min_y + 1

    filled_pos = m[2]
    print("part1:")
    for y in range(h):
        line = []
        for x in range(w):
            line.append('#' if (min_x + x, min_y + y) in filled_pos else ' ')
        print(''.join(line))

    print("Part2: {}".format(m[1]))

def main(filename):
    part1(filename)


if __name__ == "__main__":
    #main("day10-test.txt")
    main("day10.txt")
