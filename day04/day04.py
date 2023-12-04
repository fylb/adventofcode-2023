#!/usr/bin/env python3

class Card:
    def __init__(self, line):
        self.left_numbers = []
        self.right_numbers = []
        self.parse_line(line)
        self.won = 1
    def parse_line(self, line):
        left_numbers, right_numbers = line.split('|')
        left_numbers = left_numbers.split(':')[1]
        self.left_numbers = [int(n) for n in left_numbers.split(' ') if n != '']
        self.right_numbers = [int(n) for n in right_numbers.split(' ') if n != '']

    def points(self):
        common_numbers = len(set(self.left_numbers).intersection(self.right_numbers))
        #print(f"{self.left_numbers}|{self.right_numbers} -> {set(self.left_numbers).intersection(self.right_numbers)} -> {2**(common_numbers-1)}")
        if common_numbers > 0:
            return 2**(common_numbers-1)
        else:
            return 0

    def number_of_matches(self):
        return  len(set(self.left_numbers).intersection(self.right_numbers))

    def add_win(self, i):
        self.won = self.won + i

with open("input.txt") as f:
    lines = f.readlines()
    cards = [Card(line) for line in lines ]
    print(sum([card.points() for card in cards]))
    for idx, card in enumerate(cards):
        print(f"matches in card[{idx}] = {card.number_of_matches()}, current = {card.won}")
        for i in range(idx + 1, idx+1+card.number_of_matches()):
            if i < len(cards):
                cards[i].add_win(card.won)
                print(f"card[{i}] = {card.won}")
    print(sum([card.won for card in cards]))
