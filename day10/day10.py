#!/usr/bin/env python3
from functools import reduce
from math import gcd


class Tiles:
    def __init__(self):
        self.tiles = []
        self.soil = Pipe(".", -1, -1, self)

    def get_tile(self, x, y):
        if 0 <= x < len(self.tiles[0]) and 0 <= y < len(self.tiles):
            return self.tiles[y][x]
        return self.soil

class Pipe:
    def __init__(self, c, x, y, tiles):
        self.c = c
        self.x = x
        self.y = y
        self.tiles = tiles

    def __str__(self):
        return f"{self.x},{self.y}[{self.c}]"

    def __eq__(self, other):
        if other is None:
            return False
        #print(f"eq {self} / {other} => {self.x == other.x and self.y == other.y}")
        return self.x == other.x and self.y == other.y

    def next_tile(self, src_pipe):
        if self.c == ".":
            return None
        left = self.tiles.get_tile(self.x-1, self.y)
        right = self.tiles.get_tile(self.x+1, self.y)
        top = self.tiles.get_tile(self.x, self.y-1)
        bottom = self.tiles.get_tile(self.x, self.y+1)
        #print(f"{self} top {top}==src left {left} bottom{bottom} right={right} src={src_pipe}")

        match self.c:
            case "S":
                return None
            case "|":
                if top != src_pipe and (top.c == "|" or top.c == "F" or top.c == "7"):
                    return top
                if bottom != src_pipe and (bottom.c == "|" or bottom.c == "L" or bottom.c == "J"):
                    return bottom
            case "-":
                if left != src_pipe and (left.c == "-" or left.c == "F" or left.c == "L"):
                    return left
                if right != src_pipe and (right.c == "-" or right.c == "7" or right.c == "J"):
                    return right
            case "L":
                if top != src_pipe and (top.c == "|" or top.c == "F" or top.c == "7"):
                    return top
                if right != src_pipe and (right.c == "-" or right.c == "7" or right.c == "J"):
                    return right
            case "J":
                if left != src_pipe and (left.c == "-" or left.c == "F" or left.c == "L"):
                    return left
                if top != src_pipe and (top.c == "|" or top.c == "F" or top.c == "7"):
                    return top
            case "7":
                if left != src_pipe and (left.c == "-" or left.c == "F" or left.c == "L"):
                    return left
                if bottom != src_pipe and (bottom.c == "|" or bottom.c == "L" or bottom.c == "J"):
                    return bottom
            case "F":
                if right != src_pipe and (right.c == "-" or right.c == "7" or right.c == "J"):
                    return right
                if bottom != src_pipe and (bottom.c == "|" or bottom.c == "L" or bottom.c == "J"):
                    return bottom
        return None

    def initial_directions(self):
        left = self.tiles.get_tile(self.x-1, self.y)
        right = self.tiles.get_tile(self.x+1, self.y)
        top = self.tiles.get_tile(self.x, self.y-1)
        bottom = self.tiles.get_tile(self.x, self.y+1)
        directions = []
        if right.c == "-" or right.c == "7" or right.c == "J":
            directions.append(right)
        if bottom.c == "|" or bottom.c == "L" or bottom.c == "J":
            directions.append(bottom)
        if left.c == "-" or left.c == "F" or left.c == "L":
            directions.append(left)
        if top.c == "|" or top.c == "F" or top.c == "7":
            directions.append(top)
        return directions

    def loop(self):
        i = 1
        src_tile = self.initial_directions()[0]
        previous_tile = self
        while src_tile != self and src_tile is not None:
            print(f"{i} {src_tile}")
            next_tile = src_tile.next_tile(previous_tile)
            previous_tile = src_tile
            src_tile = next_tile
            i = i+1
        i = i +1
        return i//2

class InputFile:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        tiles = Tiles()
        start = None
        for y, line in enumerate(self.lines):
            tile_line = []
            tiles.tiles.append(tile_line)
            for x, c in enumerate(line.strip()):
                tile_line.append(Pipe(c, x, y, tiles))
                if c == "S":
                    start = tile_line[-1]
        print("".join(self.lines))
        print(str(start.loop()))


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
