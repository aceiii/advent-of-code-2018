#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from operator import itemgetter, attrgetter
import string
import re


class Dep(object):
    def __init__(self, c):
        self.c = c
        self.deps = set()

    def __repr__(self):
        return "Dep({}) -> {}".format(self.c, tuple(self.deps,))


class Worker(object):
    def __init__(self, c, s):
        self.c = c
        self.s = s

    def __repr__(self):
        return "Worker({}):{}".format(self.c, self.s)


def find_idle_worker(workers):
    for worker in workers:
        if worker.s == 0:
            return worker
    return None


def do_work(workers, deps):
    min_s = min(w.s for w in workers if w.s > 0)
    to_remove = set()
    for w in workers:
        w.s = max(0, w.s - min_s)
        if w.s == 0 and w.c is not None:
            to_remove.add(w.c)
            w.c = None
    for dep in deps:
        dep.deps.difference_update(to_remove)
    return min_s


def part1(filename):
    with open(filename) as file:
        deps = {}
        pattern = r"^Step ([A-Z]) must be finished before step ([A-Z]) can begin\.$"
        for line in file:
            match = re.match(pattern, line.strip())
            step1, step2 = match.groups()

            if step1 not in deps:
                deps[step1] = Dep(step1)

            if step2 not in deps:
                deps[step2] = Dep(step2)

            deps[step2].deps.add(step1)

        deps = sorted([deps[d] for d in deps], key=attrgetter('c'))
        res = []
        while deps:
            for i, dep in enumerate(deps):
                if not dep.deps:
                    res.append(dep.c)
                    break
            else:
                raise Exception("Failed")

            char = res[-1]
            deps = deps[:i] + deps[i+1:]
            for dep in deps:
                if char in dep.deps:
                    dep.deps.remove(char)

        answer = "".join(res)
        print("part1: {}".format(answer))


def part2(filename):
    with open(filename) as file:
        deps = {}
        pattern = r"^Step ([A-Z]) must be finished before step ([A-Z]) can begin\.$"
        for line in file:
            match = re.match(pattern, line.strip())
            step1, step2 = match.groups()

            if step1 not in deps:
                deps[step1] = Dep(step1)

            if step2 not in deps:
                deps[step2] = Dep(step2)

            deps[step2].deps.add(step1)

        deps = sorted([deps[d] for d in deps], key=attrgetter('c'))
        workers = [Worker(None, 0) for _ in range(5)]
        answer = 0

        while deps or any(w.s > 0 for w in workers):

            # all workers are worker on something so do that work
            if all(w.s > 0 for w in workers):
                answer += do_work(workers, deps)

            # try to fill workers
            new_deps = []
            filled_worker = False
            for i, dep in enumerate(deps):
                if dep.deps:
                    new_deps.append(dep)
                else:
                    w = find_idle_worker(workers)
                    if w:
                        w.c = dep.c
                        w.s = ord(dep.c) - ord('A') + 61
                        filled_worker = True
                    else:
                        new_deps.append(dep)
            deps = new_deps
            if filled_worker:
                # try to start over first in case all workers
                # are filled so we can do their work
                continue

            # do work because can't fill any more workers
            answer += do_work(workers, deps)

        print("part2: {}".format(answer))


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    #main("day7-test.txt")
    main("day7.txt")
