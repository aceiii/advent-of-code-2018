#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


class TreeNode(object):
    def __init__(self):
        self.meta = []
        self.children = []

    def __repr__(self):
        return "TreeNode<{}, {}> {}".format(
            len(self.children),
            len(self.meta),
            self.meta)


def parse_tree_nodes(values, offset = 0):
    num_children = values[offset]
    num_meta = values[offset + 1]

    node = TreeNode()

    child_offset = 2
    for _ in range(num_children):
        new_offset, child = parse_tree_nodes(values, offset + child_offset)
        child_offset += new_offset
        node.children.append(child)

    start_index = child_offset + offset
    node.meta = values[start_index:start_index + num_meta]

    return (child_offset + num_meta, node)


def depth_first_traversal(node, callback):
    callback(node)
    for child in node.children:
        depth_first_traversal(child, callback)


def part1(filename):
    with open(filename) as file:
        values = map(int, file.readline().split(' '))

        _, tree_head = parse_tree_nodes(values)

        metas = []
        def summize_meta(child):
            metas.extend(child.meta)

        depth_first_traversal(tree_head, summize_meta)

        answer = sum(metas)
        print("part1: {}".format(answer))


def part2(filename):
    with open(filename) as file:
        values = map(int, file.readline().split(' '))

        _, tree_head = parse_tree_nodes(values)

        def node_value(node):
            if not node.children:
                return sum(node.meta)

            val = 0
            for i in node.meta:
                if i < 1 or i > len(node.children):
                    continue
                val += node_value(node.children[i - 1])

            return val

        answer = node_value(tree_head)
        print("part2: {}".format(answer))



def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    main("day8.txt")
    #main("day8-test.txt")
