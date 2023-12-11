#!/usr/bin/env python3
from functools import reduce
from math import gcd

WEIGHT=1000000

class Tiles:
    def __init__(self):
        self.tiles = []
        self.soil = Space(".", -1, -1, self)
        self.galaxies = []

    def get_tile(self, x, y):
        if 0 <= x < len(self.tiles[0]) and 0 <= y < len(self.tiles):
            return self.tiles[y][x]
        return self.soil

    def get_galaxy(self, number):
        return self.galaxies[number-1]

    def sum_distance(self):
        s = 0
        for idx, g1 in enumerate(self.galaxies):
            if idx == len(self.galaxies) - 1:
                break
            for g2 in self.galaxies[idx+1:]:
                s = s+g1.dist(g2)
        return s

    def sum_distance2(self):
        s = 0
        for idx, g1 in enumerate(self.galaxies):
            if idx == len(self.galaxies) - 1:
                break
            for g2 in self.galaxies[idx+1:]:
                s = s+g1.dist2(g2)
        return s

    def expand(self):
        ys = []
        xs = []
        for idx, tile_line in enumerate(self.tiles):
            no_galaxy = all([tile.c == "." for tile in tile_line])
            if no_galaxy:
                ys.append(idx)
        for idx in range(len(self.tiles[0])):
            no_galaxy = all([tile[idx].c == "." for tile in self.tiles])
            if no_galaxy:
                xs.append(idx)

        xs.reverse()
        ys.reverse()
        for y in ys:
            line_for_y = [Space(".", 0, 0, self) for i in range(len(self.tiles[0]))]
            self.tiles.insert(y, line_for_y)

        for x in xs:
            for y in range(len(self.tiles)):
                self.tiles[y].insert(x, Space(".", 0, 0, self))

        for y, line in enumerate(self.tiles):
            for x, tile in enumerate(line):
                if tile.c == "#":
                    tile.number = len(self.galaxies) +1
                    self.galaxies.append(tile)
                tile.x = x
                tile.y = y

    def expand2(self):
        for idx, tile_line in enumerate(self.tiles):
            no_galaxy = all([tile.c == "." for tile in tile_line])
            if no_galaxy:
                for tile in tile_line:
                    tile.x_weight = WEIGHT

        for idx in range(len(self.tiles[0])):
            no_galaxy = all([tile[idx].c == "." for tile in self.tiles])
            if no_galaxy:
                for tile_line in self.tiles:
                    tile_line[idx].y_weight = WEIGHT

        for y, line in enumerate(self.tiles):
            for x, tile in enumerate(line):
                if tile.c == "#":
                    tile.number = len(self.galaxies) +1
                    self.galaxies.append(tile)

    def __str__(self):
        s = ""
        for line in self.tiles:
            for x in line:
                if x.x_weight > 1:
                    if x.y_weight > 1:
                        s = s+"*"
                    else:
                        s = s + "-"
                elif x.y_weight > 1:
                    s = s + "|"
                else:
                    s = s+x.c
            s=s+"\n"

        return s


class Space:
    def __init__(self, c, x, y, tiles):
        self.c = c
        self.x = x
        self.y = y
        self.tiles = tiles
        self.number = 0
        self.x_weight = 1
        self.y_weight = 1

    def __str__(self):
        if self.x_weight > 1:
            if self.y_weight > 1:
                return "*"
            else:
                return "-"
        elif self.y_weight > 1:
            return "|"
        return self.c
        #return f"{self.x},{self.y}[{self.c}]"

    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dist2(self, other):
        s = 0
        for x in range(self.x, other.x, 1 if self.x < other.x else -1):
            s = s+self.tiles.get_tile(x, self.y).y_weight
        for y in range(self.y, other.y, 1 if self.y < other.y else -1):
            s = s+self.tiles.get_tile(self.x, y).x_weight
        return s

class InputFile:
    def __init__(self, lines):
        self.lines = lines

    def parse(self):
        tiles = Tiles()
        for y, line in enumerate(self.lines):
            tile_line = []
            tiles.tiles.append(tile_line)
            for x, c in enumerate(line.strip()):
                tile_line.append(Space(c, x, y, tiles))
        print(str(tiles))
        tiles.expand2()
        print("Expanding")
        print(str(tiles))
        print(str(tiles.get_galaxy(5).dist2(tiles.get_galaxy(9))))
        print(str(tiles.get_galaxy(1).dist2(tiles.get_galaxy(7))))
        print(str(tiles.get_galaxy(3).dist2(tiles.get_galaxy(6))))
        print(str(tiles.get_galaxy(8).dist2(tiles.get_galaxy(9))))
        #print(str(tiles.sum_distance()))
        print(str(tiles.sum_distance2()))



def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
