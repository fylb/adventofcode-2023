#!/usr/bin/env python3
import os
import time

import numpy

class Beam:
    def __init__(self, tiles):
        self.tiles = tiles

    def walk(self, x, y, dir_x, dir_y):
        if x + dir_x >= self.tiles.tiles.shape[1]:
            return
        if y + dir_y >= self.tiles.tiles.shape[0]:
            return
        if x + dir_x < 0:
            return
        if y + dir_y < 0:
            return

        # os.system('clear')
        # print(f"{x},{y} {dir_x},{dir_y}")
        # print(self.tiles.str(x, y, dir_x, dir_y))
        #time.sleep(0.5)
        x = x + dir_x
        y = y + dir_y
        self.tiles.tiles[y][x].visited = True
        possibilities = self.tiles.tiles[y][x].visit([dir_x, dir_y])
        while len(possibilities) == 1:
            dir_x, dir_y = possibilities[0]
            if x + dir_x >= self.tiles.tiles.shape[1]:
                break
            if y + dir_y >= self.tiles.tiles.shape[0]:
                break
            if x + dir_x < 0:
                break
            if y + dir_y < 0:
                break
            x = x + dir_x
            y = y + dir_y
            self.tiles.tiles[y][x].visited = True
            possibilities = self.tiles.tiles[y][x].visit([dir_x, dir_y])

        if len(possibilities) > 1:
            for p in possibilities:
                self.walk(x, y, p[0], p[1])


class Tiles:
    def __init__(self, tiles):
        self.tiles = numpy.array(tiles)

    def sum(self):
        s = 0
        for y, line in enumerate(self.tiles):
            for x, c in enumerate(line):
                if c.visited:
                    s = s +1
        return s

    def reset(self):
        for y, line in enumerate(self.tiles):
            for x, c in enumerate(line):
                c.reset()

    def str(self, a_x, a_y, dir_x, dir_y):
        s = ""
        for y, line in enumerate(self.tiles):
            for x, c in enumerate(line):
                if x == a_x and y == a_y:
                    if dir_x == 1:
                        s = s + ">"
                    if dir_x == -1:
                        s = s + "<"
                    if dir_y == 1:
                        s = s + "v"
                    if dir_y == -1:
                        s = s + "^"
                else:
                    s = s + str(c)
            s = s+"\n"
        return s


class Tile:
    def __init__(self, c, x, y):
        self.c = c
        self.visited = False
        self.x = x
        self.y = y
        self.inputs = {}

    def reset(self):
        self.visited = False
        self.inputs = {}

    def visit(self, direction):
        d = f"{direction[0]}{direction[1]}"
        if d in self.inputs:
            return []
        self.inputs[d] = 1
        self.visited = True
        match self.c:
            case '.':
                return [(direction[0], direction[1])]
            case '\\':
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
        m = 0
        for x in range(tiles.tiles.shape[1]):
            print(f"x={x}  {m}")
            beam.walk(x, -1, 0, 1)
            m = max(m, tiles.sum())
            tiles.reset()
            beam.walk(x, tiles.tiles.shape[0], 0, -1)
            m = max(m, tiles.sum())
            tiles.reset()

        for y in range(tiles.tiles.shape[0]):
            print(f"y={y}  {m}")
            beam.walk(-1, y, 1, 0)
            m = max(m, tiles.sum())
            tiles.reset()
            beam.walk(tiles.tiles.shape[1], y, -1, 0)
            m = max(m, tiles.sum())
            tiles.reset()

        print(tiles)
        print(tiles.sum())


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
