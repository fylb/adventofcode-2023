#!/usr/bin/env python3


class Lines:
    def __init__(self, lines):
        self.lines = lines

    def get_numbers(self):
        for i in range(len(self.lines)):
            current_line = self.lines[i]
            if i > 0:
                previous_line = self.lines[i-1]
            else:
                previous_line = None
            if i < len(self.lines) - 1:
                next_line = self.lines[i+1]
            else:
                next_line = None

            print(previous_line)
            print(current_line)
            print(next_line)
            pos = current_line.get_index_of_next_number(0)
            while pos >= 0:
                n, start_of_n, length_of_n = current_line.get_number(pos)
                test_range = [i for i in range(pos-1, pos+length_of_n+1)]
                pos = pos + length_of_n
                pos = current_line.get_index_of_next_number(pos)
                if current_line.is_symbol(test_range[0]) or current_line.is_symbol(test_range[-1]):
                    current_line.numbers.append(n)
                    continue
                for t in test_range:
                    if previous_line is not None and previous_line.is_symbol(t):
                        current_line.numbers.append(n)
                        break
                    if next_line is not None and next_line.is_symbol(t):
                        current_line.numbers.append(n)
                        break
            print(current_line.numbers)
        print(sum(n for line in self.lines for n in line.numbers))

    def get_ratio(self):
        s = 0
        for i in range(len(self.lines)):
            current_line = self.lines[i]
            if i > 0:
                previous_line = self.lines[i-1]
            else:
                previous_line = None
            if i < len(self.lines) - 1:
                next_line = self.lines[i+1]
            else:
                next_line = None
            print(str(i))
            print(previous_line)
            print(current_line)
            print(next_line)
            pos = current_line.get_next_gear_symbol(0)
            while pos >= 0:
                adjacent_numbers = []
                for line in [previous_line, current_line, next_line]:
                    if line is not None:
                        p = pos - 1
                        while p <= pos + 1:
                            if line.is_number(p):
                                n, start_of_n, length_of_n = line.get_number(p)
                                adjacent_numbers.append(n)
                                p = start_of_n + length_of_n +1
                            else:
                                p = p+1
                if len(adjacent_numbers) == 2:
                    print(f"Found a gear, adjacent numbers = {adjacent_numbers}")
                    s = s + adjacent_numbers[0] * adjacent_numbers[1]
                pos = current_line.get_next_gear_symbol(pos+1)

        print(s)


class Line:

    def __init__(self, content):
        self.line = [c for c in content.strip()]
        self.numbers = []

    def __str__(self):
        return "".join(self.line)

    def is_symbol(self, pos):
        return 0 < pos < len(self.line) and self.line[pos] != '.' and not self.is_number(pos)

    def get_next_gear_symbol(self, pos):
        while pos < len(self.line) and self.line[pos] != '*':
            pos = pos + 1
        if pos == len(self.line):
            return -1
        else:
            return pos

    def get_index_of_next_number(self, pos):
        while pos < len(self.line) and not self.is_number(pos):
            pos = pos + 1
        if pos == len(self.line):
            return -1
        else:
            return pos

    def is_number(self, pos):
        return 0 <= pos < len(self.line) and self.line[pos].isdigit()

    def get_number(self, pos):
        while pos >= 0 and self.is_number(pos):
            pos = pos-1
        pos = pos + 1
        start = pos
        n = ""
        while pos < len(self.line) and self.is_number(pos):
            n = n + self.line[pos]
            pos = pos + 1
        return int(n), start, len(n)


class InputFile:
    def __init__(self, lines):
        self.lines = lines
        self.games = []

    def parse(self):
        lines = Lines([Line(line) for line in self.lines])
        # lines.get_numbers()
        lines.get_ratio()


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
