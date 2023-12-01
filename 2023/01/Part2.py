#!/usr/bin/env python3

#Advent of Code
#2023 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def digit_to_int(digit: str) -> int:
        match digit:
            case "1" | "one":   return 1
            case "2" | "two":   return 2
            case "3" | "three": return 3
            case "4" | "four":  return 4
            case "5" | "five":  return 5
            case "6" | "six":   return 6
            case "7" | "seven": return 7
            case "8" | "eight": return 8
            case "9" | "nine":  return 9

    def parse_calibration_value(line: str) -> int:
        valid_digits: list[str] = [*"123456789", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        found_digits: list[str] = []

        # Originally implemented with a regex, but since numbers may be overlapping
        # (e.g. "oneight" contains both "one" and "eight") and we want the last digit,
        # we can't use something like re.findall() (which would find "one" and then stop).

        for i in range(len(line)):
            for digit in valid_digits:
                if line[i:].startswith(digit):
                    found_digits.append(digit)
                    break

        return int(f"{digit_to_int(found_digits[0])}{digit_to_int(found_digits[-1])}")

    return sum(map(parse_calibration_value, puzzle_input))

def main():
    puzzle_input = util.read.as_lines()

    print(f"The sum of all the calibration values is {solve(puzzle_input)}.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["two1nine",
                                       "eightwothree",
                                       "abcone2threexyz",
                                       "xtwone3four",
                                       "4nineeightseven2",
                                       "zoneight234",
                                       "7pqrstsixteen"]), 281)

run(main)
