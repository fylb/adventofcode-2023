#!/usr/bin/env python3

class Node:
    def __init__(self, name):
        self.name = name
        self.right = None
        self.left = None

    def __str__(self):
        return f"{self.name} => ({self.left.name}, {self.right.name})"


class Direction:
    def __init__(self, line):
        self.directions = line

    def navigate(self, start_node):
        i = 0
        current_node = start_node
        found = False
        while not found:
            for c in self.directions:
                match c:
                    case "L":
                        next_node = current_node.left
                    case "R":
                        next_node = current_node.right

                print(f"{current_node} / {c} => {next_node}")
                current_node = next_node
                i = i+1
                if next_node.name == "ZZZ":
                    found = True
                    break

        return i


    def navigate2(self, nodes):
        i = 0
        current_nodes = [node for node in nodes if node.name[2] == "A"]
        found = False
        while not found:
            for c in self.directions:
                match c:
                    case "L":
                        next_nodes = [x.left for x in current_nodes]
                    case "R":
                        next_nodes = [x.right for x in current_nodes]

                if i % 1000000 == 0:
                    print(f"{i} {' '.join([str(n) for n in current_nodes])} / {c} || {' '.join([str(n) for n in next_nodes])}")
                current_nodes = next_nodes
                i = i+1
                found = all([n.name[2] == "Z" for n in next_nodes])
                if found:
                    break
        return i

class InputFile:
    def __init__(self, lines):
        self.lines = lines
        self.maps = []

    def parse(self):
        direction = Direction(self.lines[0].strip())
        nodes = {}
        for line in self.lines[2:]:
            s = line.split("=")
            node = Node(s[0].strip())
            nodes[node.name] = node

        for line in self.lines[2:]:
            s = line.split("=")
            left, right = s[1].replace("(", "").replace(")", "").split(",")
            nodes[s[0].strip()].left = nodes[left.strip()]
            nodes[s[0].strip()].right = nodes[right.strip()]

        #print(str(direction.navigate(nodes['AAA'])))
        print(str(direction.navigate2(nodes.values())))

def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()