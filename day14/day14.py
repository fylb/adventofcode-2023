#!/usr/bin/env python3
from functools import reduce
from math import gcd

import numpy as np

class Puzzle:
    def __init__(self, lines):
        self.arr = np.array(lines, dtype=object)
        self.norths = {}

    def shift_north(self):
        shift = False
        for i in range(1, self.arr.shape[0]):
            shift = shift or self.shift_row(i, -1)
        return shift

    def shift_south(self):
        shift = False
        for i in range(0, self.arr.shape[0]-1):
            shift = shift or self.shift_row(i, 1)
        return shift

    def shift_west(self):
        shift = False
        for i in range(1, self.arr.shape[1]):
            shift = shift or self.shift_column(i, -1)
        return shift

    def shift_east(self):
        shift = False
        for i in range(0, self.arr.shape[1]-1):
            shift = shift or self.shift_column(i, 1)
        return shift

    def cycle_clever(self):
        i = 0
        while i < 1000000000:
            a = self.cycle(i)
            if a != 0:
                print(a)
                i = i + a * (1000000000 // a) - a +1
            else:
                i = i+1

    def cycle(self, iteration):
        print(iteration)
        if iteration % 10 == 0:
            print(iteration)
        while self.shift_north():
            pass
        north = self.arr.data.tobytes()
        while self.shift_west():
            pass
        while self.shift_south():
            pass
        while self.shift_east():
            pass
        if north in self.norths and iteration < 990000000:
            print(f"Found it at iteration {iteration}")
            print(str(north))
            return iteration - self.norths[north]
        self.norths[str(north)] = iteration
        return 0

    def shift_row(self, row, direction):
        shift = False
        for i in range(self.arr.shape[1]):
            if self.arr[row+direction][i] == '.':
                if self.arr[row][i] == 'O':
                    self.arr[row+direction][i] = 'O'
                    self.arr[row][i] = '.'
                    shift = True
        return shift

    def shift_column(self, row, direction):
        shift = False
        for i in range(self.arr.shape[0]):
            if self.arr[i][row] == 'O':
                if self.arr[i][row+direction] == '.':
                    self.arr[i][row+direction]  = 'O'
                    self.arr[i][row] = '.'
                    shift = True
        return shift

    def load(self):
        total = 0
        for idx, row in enumerate(self.arr):
            mult = self.arr.shape[0] - idx
            total = total + len(list(filter(lambda x: x == 'O', row))) * mult
        return total


class InputFile:
    def __init__(self, lines):
        self.lines = [l.strip() for l in lines]

    def parse(self):
        a = []
        for l in self.lines:
            c = [ c for c in l]
            a.append(c)
        p = Puzzle(a)
        print(p.arr)
        while p.shift_north():
            pass
        print(p.arr)
        print(p.load())

    def parse2(self):
        a = []
        for l in self.lines:
            c = [ c for c in l]
            a.append(c)
        p = Puzzle(a)
        print(p.arr)
        p.cycle_clever()
        print(p.load())


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse2()


if __name__ == "__main__":
    main()
