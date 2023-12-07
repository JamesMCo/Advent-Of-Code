#!/usr/bin/env python3

#Advent of Code
#2023 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from enum import auto, IntEnum
from functools import total_ordering
import typing as t

def solve(puzzle_input: list[str]) -> int:
    @total_ordering
    class Card:
        name:  str
        value: int

        def __init__(self: t.Self, name: str) -> None:
            self.name = name

            match name:
                case "J": self.value = 1
                case "2": self.value = 2
                case "3": self.value = 3
                case "4": self.value = 4
                case "5": self.value = 5
                case "6": self.value = 6
                case "7": self.value = 7
                case "8": self.value = 8
                case "9": self.value = 9
                case "T": self.value = 10
                case "Q": self.value = 12
                case "K": self.value = 13
                case "A": self.value = 14

        def __str__(self: t.Self) -> str:
            return self.name

        def __eq__(self: t.Self, other: t.Self) -> bool:
            return self.value == other.value

        def __lt__(self: t.Self, other: t.Self) -> bool:
            return self.value < other.value

    class HandType(IntEnum):
        HIGH_CARD = auto()
        ONE_PAIR = auto()
        TWO_PAIR = auto()
        THREE_OF_A_KIND = auto()
        FULL_HOUSE = auto()
        FOUR_OF_A_KIND = auto()
        FIVE_OF_A_KIND = auto()

    @total_ordering
    class Hand:
        cards: list[Card]
        bid: int
        _hand_type: HandType | None

        def __init__(self: t.Self, hand_definition: str) -> None:
            cards, bid = hand_definition.split()
            self.cards = list(map(Card, cards))
            self.bid = int(bid)
            self._hand_type = None

        def __str__(self: t.Self) -> str:
            return f"{"".join(map(str, self.cards))} {self.bid}"

        def hand_with_joker_possibilities(self: t.Self) -> t.Iterable[list[Card]]:
            existing_cards = set(card.name for card in self.cards)

            possibilities: list[list[Card]] = []
            for card in self.cards:
                if card.name != "J":
                    possibilities.append([card])
                else:
                    possibilities.append([Card(name) for name in existing_cards])

            for a in possibilities[0]:
                for b in possibilities[1]:
                    for c in possibilities[2]:
                        for d in possibilities[3]:
                            for e in possibilities[4]:
                                yield [a, b, c, d, e]

        @property
        def hand_type(self: t.Self) -> HandType:
            if self._hand_type is None:
                best_hand_type = HandType.HIGH_CARD

                for candidate_hand in self.hand_with_joker_possibilities():
                    card_values = defaultdict(int)
                    for card in candidate_hand:
                        card_values[card.name] += 1

                    match sorted(card_values.values(), reverse=True):
                        case [5]:             best_hand_type = max(best_hand_type, HandType.FIVE_OF_A_KIND)
                        case [4, 1]:          best_hand_type = max(best_hand_type, HandType.FOUR_OF_A_KIND)
                        case [3, 2]:          best_hand_type = max(best_hand_type, HandType.FULL_HOUSE)
                        case [3, 1, 1]:       best_hand_type = max(best_hand_type, HandType.THREE_OF_A_KIND)
                        case [2, 2, 1]:       best_hand_type = max(best_hand_type, HandType.TWO_PAIR)
                        case [2, 1, 1, 1]:    best_hand_type = max(best_hand_type, HandType.ONE_PAIR)
                        case [1, 1, 1, 1, 1]: best_hand_type = max(best_hand_type, HandType.HIGH_CARD)

                self._hand_type = best_hand_type

            return self._hand_type

        def __eq__(self: t.Self, other: t.Self) -> bool:
            return self.cards == other.cards

        def __lt__(self: t.Self, other: t.Self) -> bool:
            if self.hand_type != other.hand_type:
                return self.hand_type < other.hand_type

            for ours, theirs in zip(self.cards, other.cards):
                if ours != theirs:
                    return ours < theirs

            # The hand types are the same and the cards are all the same
            # This hand is equal to, not less than, the other hand
            return False

    hands: list[Hand] = sorted(list(map(Hand, puzzle_input)))
    return sum(hand.bid * rank for rank, hand in enumerate(hands, 1))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total winnings are {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["32T3K 765",
                                       "T55J5 684",
                                       "KK677 28",
                                       "KTJJT 220",
                                       "QQQJA 483"]), 5905)

run(main)
