#!/usr/bin/env python
# -*- coding: utf -*-

from __future__ import print_function

import re
from operator import itemgetter


class Rect(object):
    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def __repr__(self):
        return "({0},{1},{2},{3})".format(self._x, self._y, self._w, self._h)

    def pos(self):
        return (self._x, self._y)

    def size(self):
        return (self._w, self._h)

    def min(self):
        return self.pos()

    def max(self):
        return (self._x + self._w, self._y + self._h)

    def intersects(self, rect):
        min_x1, min_y1 = self.min()
        max_x1, max_y1 = self.max()
        min_x2, min_y2 = rect.min()
        max_x2, max_y2 = rect.max()
        return (
            max_x1 > min_x2 and min_x1 < max_x2 and
            max_y1 > min_y1 and min_y1 < max_y2
        )


class Claim(object):
    def __init__(self, claim_id, rect):
        self._id = claim_id
        self._rect = rect
        self._overlap = False

    def __repr__(self):
        return "Claim[{0}]:{1}".format(self._id, self._rect)

    def id(self):
        return self._id

    def rect(self):
        return self._rect

    def markOverlap(self):
        self._overlap = True

    def isOverlapping(self):
        return self._overlap


class SpatialHash(object):
    def __init__(self, div=10):
        self._div = div
        self._map = {}

    def _key(self, x, y):
        return (x / self._div, y / self._div)

    def _keysForRect(self, rect):
        min_key = self._key(*rect.min())
        max_key = self._key(*rect.max())
        for x in xrange(min_key[0], max_key[0]+1):
            for y in xrange(min_key[1], max_key[1]+1):
                yield (x, y)

    def insert(self, rect, item):
        for key in self._keysForRect(rect):
            if key not in self._map:
                self._map[key] = set()
            self._map[key].add(item)

    def get(self, rect):
        ret = set()
        for key in self._keysForRect(rect):
            if key not in self._map:
                continue
            else:
                ret.update(self._map[key])
        return ret


def part1(filename):
    with open(filename) as file:
        squares = {}
        for line in file:
            match = re.match("^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$", line)
            claim_id, x, y, width, height = map(int, match.groups())

            for i in range(width):
                for j in range(height):
                    pos = (x + i, y + j)

                    if pos not in squares:
                        squares[pos] = 0

                    squares[pos] += 1

        wasted = 0
        for val in squares.values():
            if val > 1:
                wasted += 1

        print("part1: {0}".format(wasted))


def part2a(filename):
    with open(filename) as file:
        claims = []
        for line in file:
            match = re.match("^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$", line)
            claim_id, x, y, width, height = map(int, match.groups())
            claims.append({
                "id": claim_id,
                "x": x,
                "y": y,
                "width": width,
                "height": height,
                "overlap": False,
            })

        # Test for overlapping on x plane
        claims = sorted(claims, key=itemgetter("x"))
        prev_claims = []
        for claim in claims:
            if len(prev_claims) == 0:
                prev_claims = [claim]
                continue

            new_prev_claims = []
            for prev_claim in prev_claims:
                right_edge = prev_claim["x"] + prev_claim["width"]
                left_edge = claim["x"]

                if left_edge >= right_edge:
                    continue

                new_prev_claims.append(prev_claim)

                min_y = prev_claim["y"]
                max_y = prev_claim["y"] + prev_claim["height"]

                y1 = claim["y"]
                y2 = claim["y"] + claim["height"]

                if y1 < max_y and y2 > min_y:
                    print("Hello")
                    claim["overlap"] = True
                    prev_claim["overlap"] = True


            prev_claims = new_prev_claims

        answer = None
        for claim in claims:
            if not claim["overlap"]:
                print(claim)
                #answer = claim["id"]
                #break
        print("part2: {0}".format(answer))



def part2(filename):
    with open(filename) as file:
        claims = {}
        spatial = SpatialHash(10)

        for line in file:
            match = re.match("^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$", line)
            claim_id, x, y, width, height = map(int, match.groups())
            claim = Claim(claim_id, Rect(x, y, width, height))
            claims[claim_id] = claim
            spatial.insert(claim.rect(), claim.id())

        for claim_id in claims:
            claim = claims[claim_id]
            other_ids = spatial.get(claim.rect())
            for other_id in other_ids:
                if other_id == claim_id:
                    continue
                other_claim = claims[other_id]
                if claim.rect().intersects(other_claim.rect()):
                    claim.markOverlap()
                    other_claim.markOverlap()
            if not claim.isOverlapping():
                print("part2: {0}".format(claim.id()))
                break


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    main("day3.txt")
