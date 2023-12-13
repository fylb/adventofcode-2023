#!/usr/bin/env python3
from functools import reduce
from math import gcd

class Row:
    def __init__(self, line):
        row, possibilities = line.strip().split(" ")
        self.row = row
        self.unknown = [i for i, v in enumerate(row) if v == '?']
        self.matches = [int(i) for i in possibilities.split(",")]
        self.comb = 0

    def solve(self):
        self.combination(self.row, self.matches)
        return self.comb

    def combination(self, current_row, to_match):
        index=current_row.find("?")
        print(current_row)
        if index < 0:
            if self.valid(current_row):
                self.comb = self.comb + 1
            print(f"out of ? {self.valid(current_row)} {self.comb}")
            return
        new_row_1 = current_row[:index] + "." + current_row[index + 1:]
        if len(to_match) > 0 and index+to_match[0] < len(current_row):
            ok = all([ c == "#" or c == "?" for c in current_row[index:index+to_match[0]]])
            ok = ok and (index+to_match[0] == len(current_row)-1 or current_row[index+to_match[0]+1] == "?" or current_row[index+to_match[0]+1] == ".")
            print(f"{index} {to_match[0]} {ok} {current_row[index:index+to_match[0]]} {index+to_match[0]} {current_row[index+to_match[0]] }")
            if ok:
                new_row_2 = current_row[:index] + "#"*to_match[0] + "." + current_row[index + 1 + to_match[0]:]
                print(f"replace with #: {new_row_2}")
                self.combination(new_row_2, to_match[1:])

        self.combination(new_row_1, to_match)


    def valid(self, a_row):
        return [len(s) for s in filter(None, a_row.split('.'))] == self.matches


class InputFile:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        rows = []
        for y, line in enumerate(self.lines):
            rows.append(Row(line))
        print(rows[0].solve())



def main():
    with open('sample.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
