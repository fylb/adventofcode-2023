#!/usr/bin/env python3
import os
import time
import numpy as np
import pandas as pd

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
        while i < 1000000000-1:
            a = self.cycle(i)
            if a != 0:
                print(a)
                i = i + a * (1000000000 // a)
                while i > 1000000000:
                    i = i - a
                print(f"new i = {i}")
            else:
                i = i+1
            if i >10000:
                print(i)

    def display(self):
        # os.system('clear')
        # print(self.arr)
        # time.sleep(0.1)
        pass

    def cycle(self, iteration):
        if iteration % 1000 == 0:
            print(iteration)
        self.shift_north()
        north_hash = "".join([str(r) for r in self.arr])
        #print(north_hash)
        # north.flags.writeable = False
        # north_hash = hash(north.data)
        self.display()
        self.shift_west()
        self.display()
        self.shift_south()
        self.display()
        self.shift_east()
        self.display()
        if north_hash in self.norths and iteration < 990000000:
            print(f"Found it at iteration {iteration} / {self.norths[north_hash]}")
            #print(str(north))
            return iteration - self.norths[north_hash]
        self.norths[north_hash] = iteration
        return 0

    def shift_rows(self, direction):
        shift = False
        match direction:
            case -1:
                range_rows=list(range(self.arr.shape[0]))
                range_columns=list(range(self.arr.shape[1]))
            case 1:
                range_rows=list(range(self.arr.shape[0]))
                range_rows.reverse()
                range_columns=list(range(self.arr.shape[1]))
                range_columns.reverse()

        for row in range_rows:
            for col in range_columns:
                if self.arr[row][col] == 'O':
                    idx_dest = row+direction
                    f=False
                    while 0 <= idx_dest < self.arr.shape[0] and self.arr[idx_dest][col] == '.':
                        idx_dest = idx_dest + direction
                        f = True
                    if f:
                        self.arr[idx_dest-direction][col] = 'O'
                        self.arr[row][col] = '.'
        return shift

    def shift_columns(self, direction):
        shift = False
        match direction:
            case -1:
                range_rows=list(range(self.arr.shape[0]))
                range_columns=list(range(self.arr.shape[1]))
            case 1:
                range_rows=list(range(self.arr.shape[0]))
                range_rows.reverse()
                range_columns=list(range(self.arr.shape[1]))
                range_columns.reverse()

        for row in range_rows:
            for col in range_columns:
                if self.arr[row][col] == 'O':
                    idx_dest = col+direction
                    f=False
                    while 0 <= idx_dest < self.arr.shape[0] and  self.arr[row][idx_dest] == '.':
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
        p.cycle_clever()
        print(p.load())


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse2()


if __name__ == "__main__":
    main()
