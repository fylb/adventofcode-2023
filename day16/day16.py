#!/usr/bin/env python3
import time

import numpy

class Beam:
    def __init__(self, tiles):
        self.tiles = tiles
        self.direction = [1, 0]
        self.position = [0, 0]

    def walk(self):
        if self.direction[0] + self.position[0] >= self.tiles.tiles.shape[1]:
            return
        if self.direction[1] + self.position[1] >= self.tiles.tiles.shape[0]:
            return
        if self.direction[0] + self.position[0] < 0:
            return
        if self.direction[1] + self.position[1] < 0:
            return

        self.position[0] = self.position[0] + self.direction[0]
        self.position[1] = self.position[1] + self.direction[1]
        print(f"{self.direction} {self.position[0]},{self.position[1]}")
        b = self.tiles.tiles[self.position[1]][self.position[0]].c
        self.tiles.tiles[self.position[1]][self.position[0]].c = "o"
        print(str(self.tiles))
        self.tiles.tiles[self.position[1]][self.position[0]].c = b

        for n in self.tiles.tiles[self.position[1]][self.position[0]].visit(self.direction):
            self.direction[0] = n[0]
            self.direction[1] = n[1]
            #print(str(self.tiles))
            time.sleep(0.5)
            self.walk()


class Tiles:
    def __init__(self, tiles):
        self.tiles = numpy.array(tiles)

    def __str__(self):
        s = ""
        for line in self.tiles:
            for x in line:
                s = s + str(x)
            s = s+"\n"
        return s


class Tile:
    def __init__(self, c, x, y):
        self.c = c
        self.visited = False
        self.x = x
        self.y = y
        self.inputs = {}

    def visit(self, direction):
        d = f"{direction[0]}{direction[1]}"
        if d in self.inputs:
            return []
        self.inputs[d] = 1
        match self.c:
            case '.':
                self.visited = True
                return [(direction[0], direction[1])]
            case '\\':
                if direction[0] != 0:
                    return [(direction[1], direction[0])]
            case '/':
                return [(-direction[1], -direction[0])]
            case '|':
                if direction[0] == 0:
                    return [(direction[0], direction[1])]
                return [(0, -1),
                        (0, 1)]
            case '-':
                if direction[1] == 0:
                    return [(direction[0], direction[1])]
                return [(-1, 0),
                        (1, 0)]


    def visit2(self, direction):
        if direction in self.inputs:
            return []
        self.inputs[direction] = 1
        match self.c:
            case '.':
                self.visited = True
                return [(self.x + direction[0], self.y + direction[1], direction[0], direction[1])]
            case '\\':
                return [(self.x + direction[1], self.y + direction[0], direction[1], direction[0])]
            case '/':
                return [(self.x - direction[1], self.y - direction[0], -direction[1], -direction[0])]
            case '|':
                if direction[0] == 0:
                    return [(self.x, self.y + direction[1], direction[0], direction[1])]
                return [(self.x, self.y - 1, 0, -1),
                        (self.x, self.y + 1, 0, 1)]
            case '-':
                if direction[1] == 0:
                    return [(self.x + direction[0], self.y, direction[0], direction[1])]
                return [(self.x - 1, self.y, -1, 0),
                        (self.x + 1, self.y, 1, 0)]

    def __str__(self):
        if self.visited and self.c != 'o':
            return "#"
        return self.c


class InputFile:
    def __init__(self, lines):
        self.lines = [l.strip() for l in lines]

    def parse(self):
        a = []
        for y, line in enumerate(self.lines):
            row = []
            a.append(row)
            for x, c in enumerate(line):
                row.append(Tile(c, x, y))

        tiles = Tiles(a)
        beam = Beam(tiles)
        beam.walk()
        print(tiles)


def main():
    with open('sample.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
