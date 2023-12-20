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
        node_parts_to_negate = self.part_of.node_parts[0: self.index]
        node_parts_to_affirmate = [self]
        current = self.part_of
        parent = self.part_of.origin
        while parent is not None:
            index_in_parent = next(i for i,p in enumerate(parent.node_parts) if p.goto is not None and p.goto.name == current.name)
            node_parts_to_negate = node_parts_to_negate + parent.node_parts[0: index_in_parent]
            node_parts_to_affirmate.append(parent.node_parts[index_in_parent])
            current = parent
            parent = parent.origin

        xmas_min = XMAS("{x=1,m=1,a=1,s=1}")
        xmas_max = XMAS("{x=4000,m=4000,a=4000,s=4000}")

        for node_part in node_parts_to_affirmate:
            xmas_min, xmas_max = node_part.affirmate(xmas_min, xmas_max)
        for node_part in node_parts_to_negate:
            xmas_min, xmas_max = node_part.negate(xmas_min, xmas_max)

        print(f"must negate {[str(n) for n in node_parts_to_negate]}")
        print(f"must affirm {[str(n) for n in node_parts_to_affirmate]}")

        print(xmas_min, xmas_max)
        if xmas_min is not None:
            r = (xmas_max.x - xmas_min.x + 1) * (xmas_max.m - xmas_min.m + 1) * (xmas_max.a - xmas_min.a + 1) * (xmas_max.s - xmas_min.s + 1)
            if r > 0:
                return r
        return 0


    def affirmate(self, xmas_min, xmas_max):
        if xmas_min is None:
            return None, None
        if self.field_to_compare != '':
            if self.gt:
                current_value = getattr(xmas_min, self.field_to_compare)
                setattr(xmas_min, self.field_to_compare, max(current_value, self.value_to_compare + 1))
            else:
                current_value = getattr(xmas_max, self.field_to_compare)
                setattr(xmas_max, self.field_to_compare, min(current_value, self.value_to_compare - 1))
        return xmas_min, xmas_max

    def negate(self, xmas_min, xmas_max):
        if xmas_min is None:
            return None, None
        if self.field_to_compare != '':
            if self.gt:
                current_max = getattr(xmas_max, self.field_to_compare)
                setattr(xmas_max, self.field_to_compare, min(current_max, self.value_to_compare))
            elif not self.gt:
                current_min = getattr(xmas_min, self.field_to_compare)
                setattr(xmas_min, self.field_to_compare, max(current_min, self.value_to_compare))
        elif self.do_accept or self.do_reject:
            return None, None
        return xmas_min, xmas_max

    def __str__(self):
        return self.condition

class Node:
    def __init__(self, line):
        self.name = line.split("{")[0]
        self.line = line
        self.node_parts = []
        self.origin = None

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
        s = 0
        for node in nodes.values():
            for node_part in node.node_parts:
                if node_part.do_accept:
                    accept_nodes.append(node_part)
                    s = s + node_part.path_to_acceptance()
        print(s)

def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse2()


if __name__ == "__main__":
    main()
