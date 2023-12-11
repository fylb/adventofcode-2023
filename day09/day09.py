#!/usr/bin/env python3
from functools import reduce
from math import gcd

class Dataset:
    def __init__(self, line = '', depth=0, numbers=None):
        self.numbers = [ int(i.strip()) for i in line.split(" ")] if line != '' else numbers
        self.ancestor = None
        self.child = None
        self.depth = depth

    def solve(self):
        print(str(self))
        child_numbers = [self.numbers[i+1] - self.numbers[i] for i in range(len(self.numbers) - 1)]
        self.child = Dataset(depth=self.depth+1, numbers=child_numbers)
        self.child.ancestor = self
        if all([n==0 for n in child_numbers]):
            self.child.numbers.append(0)
            self.solve_to_top()
        else:
            self.child.solve()

    def solve_to_top(self):
        self.numbers.append(self.numbers[-1] + self.child.numbers[-1])
        print(str(self))
        if self.ancestor is not None:
            self.ancestor.solve_to_top()

    def __str__(self):
        return f"{self.depth * ' '}{' '.join([str(i) for i in self.numbers])}"

    def solve2(self):
        print(str(self))
        child_numbers = [self.numbers[i+1] - self.numbers[i] for i in range(len(self.numbers) - 1)]
        self.child = Dataset(depth=self.depth+1, numbers=child_numbers)
        self.child.ancestor = self
        if all([n==0 for n in child_numbers]):
            self.child.numbers.insert(0, 0)
            print(str(self.child))
            self.solve_to_top2()
        else:
            self.child.solve2()

    def solve_to_top2(self):
        self.numbers.insert(0, self.numbers[0] - self.child.numbers[0])
        print(str(self))
        if self.ancestor is not None:
            self.ancestor.solve_to_top2()

class InputFile:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        datasets = []
        for line in self.lines:
            dataset = Dataset(line, 0)
            datasets.append(dataset)
            dataset.solve2()
        print(str(sum([dataset.numbers[0] for dataset in datasets])))


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
