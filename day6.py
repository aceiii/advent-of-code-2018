#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from operator import itemgetter, methodcaller
import string
import re


class Point(object):
    def __init__(self, point_id, x, y):
        self.id = point_id
        self._x = x
        self._y = y

    def __repr__(self):
        return "Point[{}]:{} ({},{})".format(self.id,
                                             self.distance(),
                                             self._x,
                                             self._y)

    def addX(self, x):
        self._x += x

    def addY(self, y):
        self._y += y

    def distance(self):
        return abs(self._x) + abs(self._y)


def manhattan_dist((x1, y1), (x2, y2)):
    return abs(x2 - x1) + abs(y2 - y1)


def part1(filename):
    with open(filename) as file:
        points = []
        for line in file:
            match = re.match(r"^(\d+), (\d+)$", line)
            x, y = map(int, match.groups())
            points.append((x, y))

        min_x = min(map(itemgetter(0), points)) - 1
        min_y = min(map(itemgetter(1), points)) - 1
        max_x = max(map(itemgetter(0), points)) + 1
        max_y = max(map(itemgetter(1), points)) + 1

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        grid = []

        points = map(lambda (i, p): Point(string.ascii_letters[i],
                                          min_x - p[0] - 1, min_y - p[1] - 1),
                     enumerate(points))

        for y in range(height):
            grid.append([])
            for p in points:
                p.addY(1)

            for x in range(width):
                for p in points:
                    p.addX(1)

                points.sort(key=methodcaller('distance'))

                if points[0].distance() < points[1].distance():
                    grid[-1].append(points[0].id)
                else:
                    grid[-1].append(None)

            else:
                for p in points:
                    p.addX(-width)

        sizes = {}
        exclude = set()
        i = 0
        for row in grid:
            exclude_row = i == 0 or i == len(grid)-1

            exclude.add(row[0])
            exclude.add(row[-1])

            for c in row:
                if c is None:
                    continue

                if exclude_row:
                    exclude.add(c)

                if c not in sizes:
                    sizes[c] = 0

                sizes[c] += 1
            i += 1

        areas = filter(lambda (i, _): i not in exclude, sizes.items())
        areas.sort(key=itemgetter(1), reverse=True)

        answer = areas[0][1]
        print("part1: {}".format(answer))


def part2(filename):
    with open(filename) as file:
        points = []
        for line in file:
            match = re.match(r"^(\d+), (\d+)$", line)
            x, y = map(int, match.groups())
            points.append((x, y))

        min_x = min(map(itemgetter(0), points)) - 1
        min_y = min(map(itemgetter(1), points)) - 1
        max_x = max(map(itemgetter(0), points)) + 1
        max_y = max(map(itemgetter(1), points)) + 1

        width = max_x - min_x + 1
        height = max_y - min_y + 1

        grid = []

        points = map(lambda (i, p): Point(string.ascii_letters[i],
                                          min_x - p[0] - 1, min_y - p[1] - 1),
                     enumerate(points))

        for y in range(height):
            grid.append([])
            for p in points:
                p.addY(1)

            for x in range(width):
                for p in points:
                    p.addX(1)

                grid[-1].append(sum(map(methodcaller('distance'), points)))

            else:
                for p in points:
                    p.addX(-width)

        total = 0
        for row in grid:
            for c in row:
                if c < 10000:
                    total += 1

        answer = total
        print("part2: {}".format(answer))


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    #main("day6-test.txt")
    main("day6.txt")
