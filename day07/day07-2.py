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
                self.value = 0
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


FIVE_OF_A_KIND = 100
FOUR_OF_A_KIND = 90
FULL_HOUSE = 80
THREE_OF_A_KIND = 70
TWO_PAIRS = 60
ONE_PAIR = 50
HIGH_CARD = 40

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
        new_cards = sorted([c for c in self.cards if c.str_value != 'J'], key=lambda x: x.value, reverse=True)
        if len(new_cards) == 0:
            return FIVE_OF_A_KIND

        number_of_jokers = len([card for card in self.cards if card.str_value == 'J'])
        five_of_kind = False
        four_of_a_kind = False
        full_house = False
        three_of_a_kind = False
        two_pairs = False
        one_pair = False

        number_of_pairs = 0
        if len(new_cards) > 1:
            previous_card = new_cards[0]
            for card in new_cards[1:]:
                if card == previous_card:
                    number_of_pairs = number_of_pairs + 1
                previous_card = card

        match len(new_cards):
            case 5:
                five_of_kind = new_cards[0] == new_cards[4]
                four_of_a_kind = new_cards[0] == new_cards[3] or new_cards[1] == new_cards[4]
                full_house = (new_cards[0] == new_cards[2] and new_cards[3] == new_cards[4]) or (new_cards[0] == new_cards[1] and new_cards[2] == new_cards[4])
                three_of_a_kind = new_cards[0] == new_cards[2] or new_cards[1] == new_cards[3] or new_cards[2] == new_cards[4]
                two_pairs = number_of_pairs == 2
                one_pair = number_of_pairs == 1
            case 4:
                four_of_a_kind = new_cards[0] == new_cards[3]
                three_of_a_kind = new_cards[0] == new_cards[2] or new_cards[1] == new_cards[3]
                two_pairs = number_of_pairs == 2
                one_pair = number_of_pairs == 1
            case 3:
                three_of_a_kind = new_cards[0] == new_cards[2]
                one_pair = number_of_pairs == 1
            case 2:
                one_pair = new_cards[0] == new_cards[1]

        match number_of_jokers:
            case 0:
                if five_of_kind:
                    return FIVE_OF_A_KIND
                if four_of_a_kind:
                    return FOUR_OF_A_KIND
                if full_house:
                    return FULL_HOUSE
                if three_of_a_kind:
                    return THREE_OF_A_KIND
                if two_pairs:
                    return TWO_PAIRS
                if one_pair:
                    return ONE_PAIR
                return HIGH_CARD
            case 1:
                if four_of_a_kind:
                    return FIVE_OF_A_KIND
                if three_of_a_kind:
                    return FOUR_OF_A_KIND
                if two_pairs:
                    return FULL_HOUSE
                if one_pair:
                    return THREE_OF_A_KIND
                return ONE_PAIR
            case 2:
                if three_of_a_kind:
                    return FIVE_OF_A_KIND
                if one_pair:
                    return FOUR_OF_A_KIND
                return THREE_OF_A_KIND
            case 3:
                if one_pair:
                    return FIVE_OF_A_KIND
                return FOUR_OF_A_KIND
            case 4:
                return FIVE_OF_A_KIND
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