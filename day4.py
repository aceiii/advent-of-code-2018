#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime
from operator import itemgetter, methodcaller
import re


class GuardLog(object):
    def __init__(self, date, line):
        self._date = date
        match = re.match("^Guard #(\d+) begins shift$", line)
        if match is not None:
            self._id = int(match.groups()[0])
            self._line = "begins shift"
        else:
            self._id = None
            self._line = line

    def __repr__(self):
        return "GuardLog[{0}]({1}):{2}".format(self._id, self._date, self._line)

    def id(self):
        return self._id

    def setId(self, id):
        self._id = id

    def date(self):
        return self._date

    def fallsAsleep(self):
        return self._line == "falls asleep"

    def awoke(self):
        return self._line == "wakes up"


def part1(filename):
    with open(filename) as file:
        logs = []
        for line in file:
            match = re.match(r"^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\]", line)
            year, month, day, hour, minute = map(int, match.groups())
            date = datetime(year, month, day, hour, minute)
            log = GuardLog(date, line[19:].strip())
            logs.append(log)

        sleep_map = {}
        logs = sorted(logs, key=methodcaller('date'))
        prev_id = None
        sleep_start = None
        for log in logs:
            if log.id() is None:
                log.setId(prev_id)
            else:
                prev_id = log.id()
                if log.id() not in sleep_map:
                    sleep_map[log.id()] = {minute: 0 for minute in range(60)}

            if log.fallsAsleep():
                sleep_start = log.date().minute

            if log.awoke():
                sleep_end = log.date().minute
                for minute in range(sleep_start, sleep_end):
                    sleep_map[log.id()][minute] += 1
                sleep_start = None

        sleep_counts = map(lambda (i, s): {"id": i, "count": sum(s.values())},
                           sleep_map.items())
        sleep_counts = sorted(sleep_counts,
                              key=itemgetter("count"),
                              reverse=True)
        sleepy_id = sleep_counts[0]['id']
        sleep_minutes = sorted(sleep_map[sleepy_id].items(),
                               key=itemgetter(1), reverse=True)
        sleepy_minute = sleep_minutes[0][0]

        answer = sleepy_id * sleepy_minute
        print("part1: {0}".format(answer))


def part2(filename):
    with open(filename) as file:
        logs = []
        for line in file:
            match = re.match(r"^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\]", line)
            year, month, day, hour, minute = map(int, match.groups())
            date = datetime(year, month, day, hour, minute)
            log = GuardLog(date, line[19:].strip())
            logs.append(log)

        sleep_map = {}
        logs = sorted(logs, key=methodcaller('date'))
        prev_id = None
        sleep_start = None
        for log in logs:
            if log.id() is None:
                log.setId(prev_id)
            else:
                prev_id = log.id()
                if log.id() not in sleep_map:
                    sleep_map[log.id()] = {minute: 0 for minute in range(60)}

            if log.fallsAsleep():
                sleep_start = log.date().minute

            if log.awoke():
                sleep_end = log.date().minute
                for minute in range(sleep_start, sleep_end):
                    sleep_map[log.id()][minute] += 1
                sleep_start = None

        guards = map(lambda (i, m): (i, sorted(m.items(),
                                               key=itemgetter(1),
                                               reverse=True)),
                     sleep_map.items())

        guards = sorted(guards,
                        key=lambda g: g[1][0][1],
                        reverse=True)

        sleepy_id, sleepy_minutes = guards[0]
        answer = sleepy_id * sleepy_minutes[0][0]
        print("part2: {0}".format(answer))


def main(filename):
    part1(filename)
    part2(filename)


if __name__ == "__main__":
    #main("day4-test.txt")
    main("day4.txt")
