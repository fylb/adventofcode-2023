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
        print(f" -> {node.name}")
        self.node = node
        return True

    def evaluate(self):
        self.node.evaluate(self)
        return self.go_on()

    def __str__(self):
        return f"x={self.x},m={self.m},a={self.a},s={self.s}"


class NodePart:
    def __init__(self, condition, nodes, node, index):
        self.goto = None
        self.do_accept = False
        self.do_reject = False
        self.gt = True
        self.value_to_compare = -1
        self.field_to_compare = ''
        self.condition = condition
        self.origin = None
        self.part_of = node
        self.index = index

        if condition.find(":") < 0:
            match condition:
                case 'A':
                    self.do_accept = True
                case 'R':
                    self.do_reject = True
                case _:
                    self.goto = nodes[condition]
        else:
            self.field_to_compare = condition[0]
            operator = condition[1]
            rest_of_condition = condition[2:].split(':')
            self.value_to_compare = int(rest_of_condition[0])
            self.gt = operator == '>'

            match rest_of_condition[1]:
                case 'A':
                    self.do_accept = True
                case 'R':
                    self.do_reject = True
                case _:
                    self.goto = nodes[rest_of_condition[1]]
        if self.goto is not None:
            self.goto.origin = self.part_of

    def evaluate(self, xmas):
        # print(self.condition)
        if self.field_to_compare != '':
            value = getattr(xmas, self.field_to_compare)
            if self.gt and value > self.value_to_compare:
                if self.do_accept:
                    xmas.accept()
                elif self.do_reject:
                    xmas.reject()
                else:
                    xmas.go_to(self.goto)
                return True
            if not self.gt and value < self.value_to_compare:
                if self.do_accept:
                    xmas.accept()
                elif self.do_reject:
                    xmas.reject()
                else:
                    xmas.go_to(self.goto)
                return True
            return False
        elif self.do_accept:
            xmas.accept()
            return True
        elif self.do_reject:
            xmas.reject()
            return True
        else:
            xmas.go_to(self.goto)
            return True

    def path_to_acceptance(self):
        print(self)
        node_parts = self.part_of.node_parts[0: self.index]
        parent = self.origin
        print(self.origin)
        while parent.name != 'in':
            parent = parent.origin
            node_parts = node_parts + parent.part_of.node_parts[0: parent.index]


    def __str__(self):
        return self.condition

class Node:
    def __init__(self, line):
        self.name = line.split("{")[0]
        self.line = line
        self.node_parts = []

    def parse(self, all_nodes):
        conditions = self.line.split("{")[1][:-1]
        for index, condition in enumerate(conditions.split(",")):
            self.node_parts.append(NodePart(condition, all_nodes, self, index))


    def evaluate(self, node):
        for node_part in self.node_parts:
            if node_part.evaluate(node):
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

    def parse2(self):
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

        accept_nodes = []
        for node in nodes.values():
            for node_part in node.node_parts:
                if node_part.do_accept:
                    accept_nodes.append(node_part)
                    print(node_part)
                    print(node_part.path_to_acceptance())

def main():
    with open('sample.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse2()


if __name__ == "__main__":
    main()
