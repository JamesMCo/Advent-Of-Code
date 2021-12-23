#!/usr/bin/env python3

#Advent of Code
#2021 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import inf

def solve(puzzle_input):
    puzzle_input.insert(3, "  #D#C#B#A#")
    puzzle_input.insert(4, "  #D#B#A#C#")
    a_room = [x for x in [puzzle_input[5][3], puzzle_input[4][3], puzzle_input[3][3], puzzle_input[2][3]] if x != "."]
    b_room = [x for x in [puzzle_input[5][5], puzzle_input[4][5], puzzle_input[3][5], puzzle_input[2][5]] if x != "."]
    c_room = [x for x in [puzzle_input[5][7], puzzle_input[4][7], puzzle_input[3][7], puzzle_input[2][7]] if x != "."]
    d_room = [x for x in [puzzle_input[5][9], puzzle_input[4][9], puzzle_input[3][9], puzzle_input[2][9]] if x != "."]
    hallway = list(puzzle_input[1][1:12])
    energy_cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

    def solved(a_room, b_room, c_room, d_room):
        return a_room == ["A" for i in range(4)] and b_room == ["B" for i in range(4)] and c_room == ["C" for i in range(4)] and d_room == ["D" for i in range(4)]

    def hallway_segment(hallway, x1, x2):
        return hallway[min(x1, x2) : max(x1, x2) + 1]

    def segment_empty(s):
        return all(loc == "." for loc in s[1:-1])

    def make_moves(a_room, b_room, c_room, d_room, hallway):
        if solved(a_room, b_room, c_room, d_room):
            return 0

        letter_to_room = {"A": (a_room, 2), "B": (b_room, 4), "C": (c_room, 6), "D": (d_room, 8)}

        # Attempt to move an amphipod from the hallway into their rooms
        for i, amphipod in enumerate(hallway):
            if amphipod == ".":
                continue

            target_room, target_pos = letter_to_room[amphipod]

            if all(resting_amphipod == amphipod for resting_amphipod in target_room):
                if segment_empty(hallway_segment(hallway, i, target_pos)):
                    target_room.append(amphipod)
                    hallway[i] = "."
                    return (energy_cost[amphipod] * (abs(target_pos - i) + 4-len(target_room)+1)) + make_moves(a_room[:], b_room[:], c_room[:], d_room[:], hallway[:])

        # Attempt to move amphipods from incorrect rooms into their rooms
        for room, pos, req in [(a_room, 2, "A"), (b_room, 4, "B"), (c_room, 6, "C"), (d_room, 8, "D")]:
            if room and room[-1] != req:
                target_room, target_pos = letter_to_room[room[-1]]
                if target_room in [[], [room[-1]]]:
                    if segment_empty(hallway_segment(hallway, pos, target_pos)):
                        moving = room.pop()
                        target_room.append(moving)
                        return (energy_cost[moving] * (4-len(room) + abs(target_pos - pos) + 4-len(target_room)+1)) + make_moves(a_room[:], b_room[:], c_room[:], d_room[:], hallway[:])

        results = [inf]
        for room, pos, req in [(a_room, 2, "A"), (b_room, 4, "B"), (c_room, 6, "C"), (d_room, 8, "D")]:
            # Attempt to move an amphipod from an incorrect room into the hallway
            if room and any(amphipod != req for amphipod in room):
                for potential in [0, 1, 3, 5, 7, 9, 10]:
                    if hallway[potential] == "." and segment_empty(hallway_segment(hallway, pos, potential)):
                        moving = room.pop()
                        hallway[potential] = moving
                        results.append((energy_cost[moving] * (4-len(room) + abs(potential - pos))) + make_moves(a_room[:], b_room[:], c_room[:], d_room[:], hallway[:]))
                        hallway[potential] = "."
                        room.append(moving)

        return min(results)

    return make_moves(a_room, b_room, c_room, d_room, hallway)

def main():
    puzzle_input = util.read.as_lines()

    energy = solve(puzzle_input)

    print("The least energy required to organise the amphipods is " + str(energy) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["#############",
                                       "#...........#",
                                       "###B#C#B#D###",
                                       "  #A#D#C#A#",
                                       "  #########"]), 44169)

run(main)
