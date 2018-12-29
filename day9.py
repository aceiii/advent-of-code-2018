#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import re


class  CircleNode(object):
    def __init__(self, score, left = None, right = None):
        self.score = score

        self.left = left
        self.right = right

        if self.left is None and self.right is None:
            self.left = self
            self.right = self
        elif self.left is None:
            self.left = self.right
        elif self.right is None:
            self.right = self.left

    def __repr__(self):
        start_node = self
        current_node = start_node
        arr = []
        while True:
            arr.append(current_node.score)
            current_node = current_node.right
            if current_node is None or current_node == start_node:
                break
        return ",".join(map(str, arr))

    def append(self, score):
        right = self.right
        new_node = CircleNode(score, self, right)
        self.right = new_node
        right.left = new_node
        return new_node

    def pop(self):
        score = self.score
        right = self.right
        left = self.left

        self.right = None
        self.left = None

        if right is self or left is self:
            return (score, None)

        right.left = left
        left.right = right

        return (score, right)


def part1(filename):
    with open(filename) as file:
        for line in file:
            if line.find(':') > -1:
                line = line[:line.index(':')]
            line = line.strip()

            pattern = r"^(\d+) players; last marble is worth (\d+) points"
            match = re.match(pattern, line)
            num_players, num_marbles = map(int, match.groups())
            num_marbles += 1

            players = [0 for _ in range(num_players)]
            current_index = 0
            circle = [0]

            for score in range(1, num_marbles + 1):
                current_player = score % num_players
                if score % 23 == 0:
                    players[current_player] += score
                    current_index = (current_index - 7) % len(circle)
                    popped = circle.pop(current_index)
                    #print(popped, circle[current_index])
                    players[current_player] += popped
                    continue

                current_index = (current_index + 2) % len(circle)
                circle.insert(current_index, score)

                #print(circle)

            #print(players)
            answer = max(players)
            print("part1: {}: high score is {}".format(line, answer))


def part2(filename):
    with open(filename) as file:
        for line in file:
            if line.find(':') > -1:
                line = line[:line.index(':')]
            line = line.strip()

            pattern = r"^(\d+) players; last marble is worth (\d+) points"
            match = re.match(pattern, line)
            num_players, num_marbles = map(int, match.groups())
            num_marbles *= 100
            num_marbles += 1

            players = [0 for _ in range(num_players)]

            current_node = CircleNode(0)

            for score in range(1, num_marbles + 1):
                current_player = score % num_players

                if score % 23 == 0:
                    players[current_player] += score
                    current_node = current_node.left.left.left.left.left.left.left
                    popped, current_node = current_node.pop()
                    players[current_player] += popped
                    continue

                current_node = current_node.right.append(score)

                #print(current_node)

            #print(players)
            answer = max(players)
            print("part2: {}: high score is {}".format(line, answer))


def main(filename):
    part1(filename)
    part2(filename)


def test():
    c = CircleNode(0)
    c = c.right.append(3)
    c = c.right.right
    print(c)

if __name__ == "__main__":
    main("day9.txt")
    #main("day9-test.txt")
