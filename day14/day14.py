#!/usr/bin/env python3
from functools import reduce
from math import gcd

import numpy as np

class Puzzle:
    def __init__(self, lines):
        self.arr = np.array(lines, dtype=object)
        self.norths = {}

    def shift_north(self):
        self.shift_rows(-1)

    def shift_south(self):
        self.shift_rows(1)

    def shift_west(self):
        self.shift_columns(-1)

    def shift_east(self):
        self.shift_columns(1)

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
        print(self.arr)
        if iteration > 2:
            exit(0)
        if iteration % 1000 == 0:
            print(iteration)
        self.shift_north()
        north = self.arr.data.tobytes()
        self.shift_west()
        self.shift_south()
        self.shift_east()
        if north in self.norths and iteration < 990000000:
            print(f"Found it at iteration {iteration}")
            print(str(north))
            return iteration - self.norths[north]
        self.norths[str(north)] = iteration
        return 0

    def shift_rows(self, direction):
        shift = False
        for row in range(self.arr.shape[0]):
            for col in range(self.arr.shape[1]):
                if self.arr[row][col] == 'O':
                    idx_dest = row+direction
                    f=False
                    while 0 <= idx_dest < self.arr.shape[0] - 1 and self.arr[idx_dest][col] == '.':
                        idx_dest = idx_dest + direction
                        f = True
                    if f:
                        self.arr[idx_dest-direction][col] = 'O'
                        self.arr[row][col] = '.'
        return shift

    def shift_columns(self, direction):
        shift = False
        for row in range(self.arr.shape[0]):
            for col in range(self.arr.shape[1]):
                if self.arr[row][col] == 'O':
                    idx_dest = col+direction
                    f=False
                    while 0 <= idx_dest < self.arr.shape[0] - 1 and  self.arr[row][idx_dest] == '.':
                        idx_dest = idx_dest + direction
                        f = True
                    if f:
                        self.arr[row][idx_dest-direction] = 'O'
                        self.arr[row][col] = '.'
        return shift
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
                    self.arr[i][row+direction] = 'O'
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
            c = [c for c in l]
            a.append(c)
        p = Puzzle(a)
        print(p.arr)
        p.cycle_clever()
        print(p.load())


def main():
    with open('sample.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse2()


if __name__ == "__main__":
    main()
