#!/usr/bin/env python3

#Advent of Code
#2023 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from enum import auto, IntEnum
import typing as t

def solve(puzzle_input: list[str]) -> int:
    def make_card(c: str) -> int:
        match c:
            case "2": return 2
            case "3": return 3
            case "4": return 4
            case "5": return 5
            case "6": return 6
            case "7": return 7
            case "8": return 8
            case "9": return 9
            case "T": return 10
            case "J": return 11
            case "Q": return 12
            case "K": return 13
            case "A": return 14

    class HandType(IntEnum):
        HIGH_CARD = auto()
        ONE_PAIR = auto()
        TWO_PAIR = auto()
        THREE_OF_A_KIND = auto()
        FULL_HOUSE = auto()
        FOUR_OF_A_KIND = auto()
        FIVE_OF_A_KIND = auto()

    class Hand:
        cards: list[int]
        bid: int
        _hand_type: HandType | None

        def __init__(self: t.Self, hand_definition: str) -> None:
            cards, bid = hand_definition.split()
            self.cards = list(map(make_card, cards))
            self.bid = int(bid)
            self._hand_type = None

        def __str__(self: t.Self) -> str:
            return f"{self.cards} {self.bid}"

        @property
        def hand_type(self: t.Self) -> HandType:
            if self._hand_type is None:
                card_values = defaultdict(int)
                for card in self.cards:
                    card_values[card] += 1

                match sorted(card_values.values(), reverse=True):
                    case [5]:             self._hand_type = HandType.FIVE_OF_A_KIND
                    case [4, 1]:          self._hand_type = HandType.FOUR_OF_A_KIND
                    case [3, 2]:          self._hand_type = HandType.FULL_HOUSE
                    case [3, 1, 1]:       self._hand_type = HandType.THREE_OF_A_KIND
                    case [2, 2, 1]:       self._hand_type = HandType.TWO_PAIR
                    case [2, 1, 1, 1]:    self._hand_type = HandType.ONE_PAIR
                    case [1, 1, 1, 1, 1]: self._hand_type = HandType.HIGH_CARD

            return self._hand_type

        def __lt__(self: t.Self, other: t.Self) -> bool:
            # According to https://docs.python.org/3/library/functions.html#sorted
            # it is sufficient (though not recommended) to
            # only implement __lt__ for sorting.

            if self.hand_type != other.hand_type:
                return self.hand_type < other.hand_type

            for ours, theirs in zip(self.cards, other.cards):
                if ours != theirs:
                    return ours < theirs

            # The hand types are the same and the cards are all the same
            # This hand is equal to, not less than, the other hand
            return False

    hands: list[Hand] = sorted(map(Hand, puzzle_input))
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
                                       "QQQJA 483"]), 6440)

run(main)
