#!/usr/bin/env python3
import threading
import concurrent.futures

class SourceToDestination:
  def __init__(self, src, dest, location_range):
    self.src = src
    self.dest = dest
    self.location_range = location_range

  def contains(self, seed):
    return self.src <= seed < self.src + self.location_range

  def dest_location(self, seed):
    return seed + self.dest - self.src


class Map:
  def __init__(self, src, dest):
    self.src = src
    self.dest = dest
    self.paths = []
    self.next_map = None

  def location_of_seed(self, seed):
    #print(f"{self.src} to {self.dest}")
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
    seeds = [int(s) for s in self.lines[0].split(':')[1].strip().split(' ')]
    current_map = Map("seed", "soil")
    first_map = current_map
    for i in range(3, len(self.lines)):
      line = self.lines[i].strip()
      if line == '':
        continue
      if line[0].isdigit():
        path = line.split(' ')
        current_map.paths.append(SourceToDestination(int(path[1]), int(path[0]), int(path[2])))
      else:
        src_and_dest = line.split("-")
        current_map.next_map = Map(src_and_dest[0], src_and_dest[2])
        current_map = current_map.next_map

    lowest_location = seeds[0]
    for s in seeds:
      m = first_map
      current_location = s
      while m is not None:
        new_location = m.location_of_seed(current_location)
        m = m.next_map
        current_location = new_location
      lowest_location = min(lowest_location, current_location)
    print(lowest_location)

    def get_min(idx):
      lowest_location = 100000000000000000000
      print(f"testing {int(second_seeds[idx])} over {int(second_seeds[idx*2+1])}")
      start = int(second_seeds[idx*2])
      end = start + int(second_seeds[idx*2+1])
      seeds = range(start, end)
      for s in seeds:
        if s % 500000 == 0:
          print(f"testing {idx} {s}, progress={100*((s-start)/(end-start))}")
        m = first_map
        current_location = s
        while m is not None:
          new_location = m.location_of_seed(current_location)
          m = m.next_map
          current_location = new_location
        lowest_location = min(lowest_location, current_location)
      print(f"testing {idx} result={lowest_location}")
      return lowest_location

    second_seeds = self.lines[0].split(':')[1].strip().split(' ')

    with concurrent.futures.ThreadPoolExecutor() as executor:
      futures = [ executor.submit(get_min, i) for i in range(len(second_seeds)//2)]
      returned_values = [ future.result() for future in concurrent.futures.as_completed(futures) ]
      print(returned_values)
      print(f"min overall: {min(returned_values)}")

def main():
  with open('input.txt', 'r') as input_file:
    f = InputFile(input_file.readlines())
  f.parse()


if __name__ == "__main__":
  main()