#!/usr/bin/env python3
import re


class Bag:
    def __init__(self):
        self.red = 0
        self.blue = 0
        self.green = 0

    def update(self, color, nb):
        match color:
            case "red":
                self.red = max(self.red, nb)
            case "blue":
                self.blue = max(self.blue, nb)
            case "green":
                self.green = max(self.green, nb)

    def min_total(self):
        return self.blue + self.green + self.red

    def possible(self, red, green, blue):
        return self.blue <= blue and self.red <= red and self.green <= green

    def __str__(self):
        return f"red: {self.red}, blue: {self.blue}, green: {self.green}"

    def power(self):
        return self.red * self.green * self.blue


class Game:
    def __init__(self, id):
        self.id = id
        self.bag = Bag()

    def __str__(self):
        return f"{self.id}: [{self.bag}], 12: {self.bag.possible(12)}, 13: {self.bag.possible(12)}, 14: {self.bag.possible(12)}"


class InputFile:
    def __init__(self, lines):
        self.lines = lines
        self.games = []

    def parse(self):
        i = 0
        j=0
        for line in self.lines:
            r = re.findall("Game ([0-9]+): (.+)$", line.strip())[0]
            g = Game(int(r[0]))
            print(line)
            for draw in r[1].split(';'):
                for ball in draw.split(","):
                    colors = re.findall("([0-9]+) (red|green|blue)", ball)[0]
                    g.bag.update(colors[1].strip(), int(colors[0].strip()))
            if g.bag.possible(12, 13, 14):
                i = i + g.id
            print(i)
            j = j + g.bag.power()
            print(j)


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()