#!/usr/bin/env python3
import os
import time

import numpy

class XMAS:
    def __init__(self, line):
        a = line.split(",")
        self.x = int(a[0].split('=')[1])
        self.m = int(a[1].split('=')[1])
        self.a = int(a[2].split('=')[1])
        self.s = int(a[3].split('=')[1][:-1])
        self.rejected = False
        self.accepted = False
        self.node = None

    def sum(self):
        return self.a + self.m + self.s + self.x

    def accept(self):
        self.accepted = True

    def reject(self):
        self.rejected = True

    def go_on(self):
        return not self.rejected and not self.accepted

    def go_to(self, node):
        self.node = node
        return True

    def evaluate(self):
        return self.node.evaluate(self)

    def __str__(self):
        return f"x={self.x},m={self.m},a={self.a},s={self.s}"
class Node:
    def __init__(self, line):
        self.name = line.split("{")[0]
        self.line = line
        self.lambdas = []
    def parse(self, all_nodes):
        conditions = self.line.split("{")[1][:-1]
        for condition in conditions.split(","):
            if condition.find(":") < 0:
                def test(n):
                    return True

                def action(n):
                    n.go_to(all_nodes[condition])
            else:
                match condition[0]:
                    case 'x':
                        def field_getter(n):
                            return n.x
                    case 'm':
                        def field_getter(n):
                            return n.m
                    case 'a':
                        def field_getter(n):
                            return n.a
                    case 's':
                        def field_getter(n):
                            return n.s

                cond = condition[1]
                rest_of_condition = condition[2:].split(':')
                value = int(rest_of_condition[0])
                match cond:
                    case '>':
                        def test(n):
                            return field_getter(n) > value
                    case '<':
                        def test(n):
                            return field_getter(n) < value
                match rest_of_condition[1]:
                    case 'A':
                        def action(n):
                            n.accept()
                            return True
                    case 'R':
                        def action(n):
                            n.reject()
                            return True
                    case _:
                        def action(n):
                            n.go_to(all_nodes[rest_of_condition[1]])
                            return False
            def complete_lambda(n):
                if test(n):
                    return action(n)
                return False
            self.lambdas.append(complete_lambda)

    def evaluate(self, node):
        for l in self.lambdas:
            if l(node):
                return True
        return False

    def __str__(self):
        return f"{self.name}"
class InputFile:
    def __init__(self, lines):
        self.lines = [l.strip() for l in lines]

    def parse(self):
        nodes = dict()
        xmases = []

        parse_nodes = True
        for line in self.lines:
            if line == '':
                parse_nodes = False
                continue
            if parse_nodes:
                node = Node(line)
                nodes[node.name] = node
            else:
                xmases.append(XMAS(line))

        for n in nodes.values():
            n.parse(nodes)

        for xmas in xmases:
            xmas.node = nodes['in']
            while xmas.evaluate():
                pass
        print(sum([n.sum() for n in xmases if n.accepted]))


def main():
    with open('sample.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
