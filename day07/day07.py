#!/usr/bin/env python3

class Card:
    def __init__(self, value):
        match value:
            case 'A':
                self.value = 14
            case 'K':
                self.value = 13
            case 'Q':
                self.value = 12
            case 'J':
                self.value = 11
            case 'T':
                self.value = 10
            case _:
                self.value = int(value)
        self.str_value = value

    def __str__(self):
        return self.str_value

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value
        return False

    def __lt__(self, other):
        if isinstance(other, Card):
            return self.value < other.value
        return False

class Hand:
    def __init__(self, line):
        cards, bid = line.split(' ')
        self.bid = int(bid)
        self.cards = [Card(a) for a in cards]
        self.score = self.score()
        self.rank = 0

    def __str__(self):
        return "".join(map(str, self.cards)) + " " + str(self.bid) + " score="+str(self.score)

    def __lt__(self, other):
        if self.score == other.score:
            # compare cards
            for mycard, other_card in zip(self.cards, other.cards):
                if mycard != other_card:
                    return mycard < other_card
        return self.score < other.score

    def score(self):
        new_cards = sorted(self.cards, key=lambda x: x.value, reverse=True)
        if new_cards[0] == new_cards[4]:
            # five of a kind
            return 100
        if new_cards[0] == new_cards[3] or new_cards[1] == new_cards[4]:
            # four of a kind
            return 90
        if (new_cards[0] == new_cards[2] and new_cards[3] == new_cards[4]) or (new_cards[0] == new_cards[1] and new_cards[2] == new_cards[4]):
            # full house
            return 80
        if new_cards[0] == new_cards[2] or new_cards[1] == new_cards[3] or new_cards[2] == new_cards[4]:
            # three of a kind
            return 70
        number_of_pairs = 0
        previous_card = new_cards[0]
        for card in new_cards[1:]:
            if card == previous_card:
                number_of_pairs = number_of_pairs + 1
            previous_card = card
        if number_of_pairs == 2:
            return 60
        if number_of_pairs == 1:
            return 50
        return 40


class InputFile:
    def __init__(self, lines):
        self.lines = lines
        self.maps = []

    def parse(self):
        hands = [Hand(s) for s in self.lines]
        print("input: ")
        for hand in hands:
            print(hand)
        hand_sorted = sorted(hands)
        print("sorted: ")
        for idx, hand in enumerate(hand_sorted):
            hand.rank = idx + 1
        print(sum([hand.rank * hand.bid for hand in hands]))

def main():
    with open('input.txt', 'r') as input_file:
        f = InputFile(input_file.readlines())
    f.parse()


if __name__ == "__main__":
    main()