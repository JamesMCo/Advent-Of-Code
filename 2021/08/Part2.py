#!/usr/bin/env python3

#Advent of Code
#2021 Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    total = 0

    for entry in puzzle_input:
        input_values, output_values = [half.split() for half in entry.split(" | ")]
        input_values = sorted([set(v) for v in input_values], key=lambda x: len(x))
        # Sort input values by length so that certain sets of numbers (e.g. 2, 3 and 5 with 5 segments)
        # are in predictable locations, even if their order within the group is not known

        numbers  = {number: None for number in range(10)}
        numbers[1] = 0
        numbers[4] = 2
        numbers[7] = 1
        numbers[8] = 9
        segment_c = None

        # 8 - 6 = c (upper right)
        # Check whether segment is correct by checking if 8 - candidate is in 1 (only true for 6)
        for candidate in (6, 7, 8):
            if (input_values[numbers[8]] - input_values[candidate]).pop() in input_values[numbers[1]]:
                numbers[6] = candidate
                segment_c = (input_values[numbers[8]] - input_values[numbers[6]]).pop()
                break

        # c is not in 5
        for candidate in (3, 4, 5):
            if segment_c not in input_values[candidate]:
                numbers[5] = candidate
                break

        # 5 + c = 9
        for candidate in set([6, 7, 8]) - set([numbers[6]]):
            if input_values[candidate] == input_values[numbers[5]] | set([segment_c]):
                numbers[9] = candidate
                break

        # 0 is remaining 6 segment number
        numbers[0] = (set([6, 7, 8]) - set([numbers[6], numbers[9]])).pop()

        # Length of 3 - 7 is 2 (d and g)
        # Length of 2 - 7 is 3 (d, e and g)
        for candidate in set([3, 4, 5]) - set([numbers[5]]):
            if len(input_values[candidate] - input_values[numbers[7]]) == 2:
                numbers[3] = candidate
            else:
                numbers[2] = candidate

        mapping = {n: input_values[numbers[n]] for n in numbers}

        display = 0
        for pos, digit in enumerate(output_values):
            display += [n for n in mapping if mapping[n] == set(digit)].pop() * 10**(3 - pos)
        total += display

    return total

def main():
    puzzle_input = util.read.as_lines()

    output_value_sum = solve(puzzle_input)

    print("The sum of the output values is " + str(output_value_sum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"]), 5353)

    def text_ex2(self):
        return self.assertEqual(solve(["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
                                       "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
                                       "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
                                       "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
                                       "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
                                       "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
                                       "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
                                       "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
                                       "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
                                       "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"]), 61229)

run(main)
