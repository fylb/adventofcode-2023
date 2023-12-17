#!/usr/bin/env python3
import concurrent
import concurrent.futures
import re


class Row:
    def __init__(self, i, line, second=False):
        row, possibilities = line.strip().split(" ")
        if second:
            self.row = "?".join([row for i in range(5)])
            self.matches = [int(i) for i in possibilities.split(",")]
            self.matches = self.matches + self.matches + self.matches + self.matches + self.matches
        else:
            self.row = row
            self.matches = [int(i) for i in possibilities.split(",")]
        self.i = i
        self.comb = 0


    def solve(self):
        print(self.matches)
        self.combination(self.row)
        return self.comb

    def solve2(self):
        print(f"{self.row} {self.matches}")
        self.combination2(0, self.row, self.matches)
        print(f"{self.i} {self.row} {self.matches} ====> {self.comb}")
        return self.comb

    def combination(self, current_row):
        index = current_row.find("?")
        if index < 0:
            if self.valid(current_row):
                self.comb = self.comb + 1
            return
        new_row_1 = current_row[:index] + "." + current_row[index + 1:]
        new_row_2 = current_row[:index] + "#" + current_row[index + 1:]
        self.combination(new_row_2)
        self.combination(new_row_1)

    def combination2(self, index, current_row, to_match):
        #print(f"{index} {current_row}")
        if not self.possible(index, current_row, to_match):
            return
        if index > len(current_row)-1 or len(to_match) == 0 or current_row.find('?') < 0:
            if self.valid(current_row):
                self.comb = self.comb + 1
            return

        match current_row[index]:
            case '.':
                while current_row[index] == '.' and index < len(current_row):
                    index = index + 1
                self.combination2(index, current_row, to_match)
            case '?' | '#':
                if len(to_match) > 0 and index+to_match[0] < len(current_row):
                    ok = all([c == "#" or c == "?" for c in current_row[index:index+ to_match[0]]])
                    ok = ok and (current_row[index + to_match[0]] == "?" or current_row[index + to_match[0]] == ".")
                    if ok:
                        new_row_2 = current_row[:index] + "#" * to_match[0] + "." + current_row[index + 1 + to_match[0]:]
                        self.combination2(index + to_match[0], new_row_2, to_match[1:])
                elif len(to_match) == 1 and index+to_match[0] == len(current_row):
                    ok = all([c == "#" or c == "?" for c in current_row[index:index+ to_match[0]]]) and len(to_match) == 1
                    if ok:
                        new_row_2 = current_row[:index] + "#" * to_match[0] + "." + current_row[index + 1 + to_match[0]:]
                        self.combination2(index + to_match[0], new_row_2, to_match[1:])

                if current_row[index] == '?':
                    new_row_1 = current_row[:index] + "." + current_row[index + 1:]
                    self.combination2(index, new_row_1, to_match)

    def valid(self, a_row):
        return [len(s) for s in filter(None, a_row.replace("?", ".").split('.'))] == self.matches

    def possible(self, index, a_row, to_match):
        s = a_row[index:]
        if s.count('#') > sum(to_match):
            return False
        if s.count('##') > sum(filter(lambda x: x > 1, to_match)):
            return False
        if s.count('###') > sum(filter(lambda x: x > 2, to_match)):
            return False
        return True


class InputFile:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        rows = []
        for y, line in enumerate(self.lines):
            rows.append(Row(y, line, second=True))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [ executor.submit(r.solve2) for r in rows ]
            returned_values = [ future.result() for future in concurrent.futures.as_completed(futures) ]
            print(returned_values)
            print(f"total overall: {sum(returned_values)}")
        #print(sum([r.solve2() for r in rows]))
        print("should be 525152")


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
