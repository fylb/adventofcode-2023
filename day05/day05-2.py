#!/usr/bin/env python3


class SourceToDestination:
    def __init__(self, src, dest, location_range):
        self.src = src
        self.dest = dest
        self.location_range = location_range
        self.delta = src- dest

    def contains(self, seed):
        return self.src <= seed < self.src + self.location_range

    def contains_range(self, a_range):
        if self.src > a_range.dest or self.src + self.location_range <= a_range.src:
            print(f"{a_range} not in {self} ")
            return None, [a_range]

        start = max(self.src, a_range.src)
        end = min(self.src + self.location_range - 1, a_range.dest)

        remaining_ranges = []
        if self.src > a_range.src:
            remaining_ranges.append(Range(a_range.src, self.src - a_range.src))
        if self.src + self.location_range < a_range.dest:
            remaining_ranges.append(Range(self.src + self.location_range, a_range.dest-self.src - self.location_range +1))

        matching_range = Range(self.dest_location(start), end + 1 - start)
        print(f"{a_range} in {self} => match on ([{start}, {end}] => {matching_range}) , remaining = {' '.join([str(r) for r in remaining_ranges])} ")
        return matching_range, remaining_ranges

    def dest_location(self, seed):
        return seed - self.delta

    def __str__(self):
        return f"([{self.src}, {self.src + self.location_range - 1}] => [{self.dest}, {self.dest + self.location_range - 1}])"

class Range:
    def __init__(self, src, length_of_range):
        self.src = src
        self.dest = src + length_of_range - 1

    def __str__(self):
        return f"[{self.src},{self.dest}]"


class Map:
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
        self.paths = []
        self.next_map = None

    def location_of_range(self, a_range):
        print(f"Get ranges for {a_range} in {self}")
        ranges_to_process = [a_range]
        processed_ranges = []
        for path in self.paths:
            new_ranges_to_process = []
            for range_to_process in ranges_to_process:
                if len(ranges_to_process) == 0:
                    break
                in_range, remaining = path.contains_range(range_to_process)
                if in_range is not None:
                    processed_ranges.append(in_range)
                new_ranges_to_process = new_ranges_to_process + remaining
            ranges_to_process = new_ranges_to_process

        print(
            f"locations of range {a_range} in {self}: {' '.join([str(r) for r in processed_ranges])} match, unmatched: {' '.join([str(r) for r in ranges_to_process])}")
        return processed_ranges + ranges_to_process

    def __str__(self):
        return f"{self.src} to {self.dest}"
    def location_of_seed(self, seed):
        # print(f"{self.src} to {self.dest}")
        for path in self.paths:
            if path.contains(seed):
                # print(f"special path found, {self.dest} = {path.dest_location(seed)}")
                return path.dest_location(seed)
        # print(f"no special path {self.dest} = {seed}")
        return seed


class InputFile:
    def __init__(self, lines):
        self.lines = lines
        self.maps = []

    def parse(self):

        current_map = Map("seed", "soil")
        first_map = current_map
        for i in range(3, len(self.lines)):
            line = self.lines[i].strip()
            if line == '':
                continue
            if line[0].isdigit():
                path = line.split(' ')
                current_map.paths.append(
                    SourceToDestination(int(path[1]), int(path[0]),
                                        int(path[2])))
            else:
                src_and_dest = line.split("-")
                current_map.next_map = Map(src_and_dest[0], src_and_dest[2])
                current_map = current_map.next_map

        seeds = self.lines[0].split(':')[1].strip().split(' ')
        ranges = [Range(int(seeds[2 * i]), int(seeds[2 * i + 1])) for i in
                       range(len(seeds) // 2)]
        current_map = first_map
        # ranges = [ Range(82, 1) ]
        while current_map is not None:
            new_ranges = []
            for a_range in ranges:
                new_ranges = new_ranges + current_map.location_of_range(a_range)
            ranges = new_ranges
            current_map = current_map.next_map

        print(min([ a_range.src for a_range in ranges]))


def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()
