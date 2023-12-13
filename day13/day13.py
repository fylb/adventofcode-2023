#!/usr/bin/env python3
from functools import reduce
from math import gcd

import numpy as np

class Puzzle:
    def __init__(self, lines):
        self.arr = np.array(lines, dtype=object)

    def solve(self):
        for i in range(self.arr.shape[1]):
            if self.symetry_vertical(i) > 0:
                return i+1
        for i in range(self.arr.shape[0]):
            if self.symetry_horizontal(i) > 0:
                return 100*(i+1)

    def solve2(self):
        current_solve = self.solve()
        for y in range(self.arr.shape[1]):
            for x in range(self.arr.shape[0]):
                c = self.arr[x, y]
                if c == 1:
                    self.arr[x,y] = 0
                else:
                    self.arr[x,y] = 1
                for i in range(self.arr.shape[0]):
                    if self.symetry_horizontal(i) > 0:
                        if 100*(i+1) != current_solve:
                            print(self.arr)
                            return 100*(i+1)
                self.arr[x,y] = c

        for y in range(self.arr.shape[1]):
            for x in range(self.arr.shape[0]):
                c = self.arr[x, y]
                if c == 1:
                    self.arr[x,y] = 0
                else:
                    self.arr[x,y] = 1
                for i in range(self.arr.shape[1]):
                    if self.symetry_vertical(i):
                        if i+1 != current_solve:
                            print(self.arr)
                            return i+1
                self.arr[x,y] = c
        print(self.arr)

    def symetry_vertical(self, idx):
        symetry = True
        tested = False
        for i in range(self.arr.shape[1]):
            if idx-i < 0 or idx+i+1 >= self.arr.shape[1]:
                break
            tested = True
            symetry = symetry and np.array_equal(self.arr[:, idx-i], self.arr[:, idx+i+1])
            if not symetry:
                break
        return symetry and tested

    def symetry_horizontal(self, idx):
        symetry = True
        tested = False
        for i in range(self.arr.shape[0]):
            if idx-i < 0 or idx+i+1 >= self.arr.shape[0]:
                break
            tested = True
            symetry = symetry and np.array_equal(self.arr[idx-i, :], self.arr[idx+i+1, :])
            if not symetry:
                break
        return symetry and tested


class InputFile:
    def __init__(self, lines):
        self.lines = [ l.strip() for l in lines ]

    def parse(self):
        puzzles = []
        lines = []
        for y, line in enumerate(self.lines):
            if line == '':
                p = Puzzle(lines)
                puzzles.append(p)
                lines = []
            else:
                lines.append([1 if s=='#' else 0 for s in line])

        p = Puzzle(lines)
        puzzles.append(p)
        print(sum([p.solve2() for p in puzzles]))



def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
