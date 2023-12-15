#!/usr/bin/env python3
from functools import reduce
from math import gcd

import numpy as np
from collections import OrderedDict

class Hash:
    def __init__(self, s):
        self.s = s

    def hash(self):
        v = 0
        for c in self.s:
            a = ord(c)
            v = v + a
            v = v * 17
            v = v % 256
        return v


class Lens:
    def __init__(self, s):
        if s.find("=") > 0:
            a = s.split("=")
            self.label = a[0]
            self.focal_length = int(a[1])
            self.remove = False
        else:
            self.label=s.split("-")[0]
            self.focal_length = 0
            self.remove = True
        self.label_hash = self.hash()

    def hash(self):
        v = 0
        for c in self.label:
            a = ord(c)
            v = v + a
            v = v * 17
            v = v % 256
        return v

    def __hash__(self):
        return self.label_hash

    def __str__(self):
        return f"[{self.label} {self.focal_length}]"

class Box:
    def __init__(self, id):
        self.lenses = OrderedDict()
        self.id = id

    def __hash__(self):
        return self.id

    def remove(self, lens):
        try:
            self.lenses.pop(lens.label)
        except:
            pass

    def replace(self, lens):
        self.lenses[lens.label] = lens

    def __str__(self):
        return f"Box {self.id}: {' '.join([str(l) for l in self.lenses.values() ])}"

    def value(self):
        v = 0
        box_number = self.id + 1
        for i, lens in enumerate(self.lenses.values()):
            v = v + (i+1) * lens.focal_length
        return v * box_number
class InputFile:
    def __init__(self, lines):
        self.line = [l.strip() for l in lines][0]

    def parse(self):
        hashes = []
        for to_hash in self.line.split(","):
            hashes.append(Hash(to_hash))
        print(sum([h.hash() for h in hashes]))

    def parse2(self):
        boxes = dict()
        for lens in self.line.split(","):
            print(lens)
            l = Lens(lens)
            box = boxes.setdefault(l.label_hash, Box(l.label_hash))
            if l.remove:
                box.remove(l)
            else:
                box.replace(l)
            for k, v in boxes.items():
                print(f"{k} {v}")
            print("")
        print(sum([b.value() for b in boxes.values()]))

def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse2()


if __name__ == "__main__":
    main()
