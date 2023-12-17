#!/usr/bin/env python3

#Advent of Code
#2023 Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    puzzle_input: list[list[int]] = [[int(n) for n in line] for line in puzzle_input]
    target: tuple[int, int] = (len(puzzle_input[0]) - 1, len(puzzle_input) - 1)

    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x <= target[0] and 0 <= y <= target[1]

    # To adapt my part 1 solution to part 2, all
    # I needed to do was to change the steps considered
    # (line 67 in part 1, line 43 in part 2) from
    # 1..3 to 4..10 (though, since Python's ranges are
    # not inclusive of the upper bound, 1..4 and 4..11)

    queue: list[tuple[tuple[int, int], str, int]] = [((0, 0), "initial_state", 0)]
    seen: dict[tuple[tuple[int, int], str], int] = {}
    while queue:
        coord, direction, length = queue.pop()
        if (coord, direction) in seen and seen[(coord, direction)] < length:
            # Check that we've not already been here in this exact state, but with a shorter length
            # Even though we perform this check when queueing a state, it might be possible
            # for the length to be beaten by an earlier queued state, and so we check in both places.
            continue

        if coord == target:
            # Dijkstra's algorithm means that, if we are seeing the target for the first time,
            # this is the shortest total cost to reach the target
            return length
        else:
            neighbours: list[tuple[tuple[int, int], str, int]] = []
            x, y = coord

            for steps in range(4, 11):
                if direction not in "ns":
                    # Go North
                    if in_bounds(x, y - steps):
                        neighbours.append(((x, y - steps), "n", length + sum(puzzle_input[y - intermediate][x] for intermediate in range(1, steps + 1))))
                    # Go South
                    if in_bounds(x, y + steps):
                        neighbours.append(((x, y + steps), "s", length + sum(puzzle_input[y + intermediate][x] for intermediate in range(1, steps + 1))))
                if direction not in "ew":
                    # Go East
                    if in_bounds(x + steps, y):
                        neighbours.append(((x + steps, y), "e", length + sum(puzzle_input[y][x + intermediate] for intermediate in range(1, steps + 1))))
                    # Go West
                    if in_bounds(x - steps, y):
                        neighbours.append(((x - steps, y), "w", length + sum(puzzle_input[y][x - intermediate] for intermediate in range(1, steps + 1))))

            for neighbour in neighbours:
                if neighbour not in queue:
                    if not ((neighbour[0], neighbour[1]) in seen and seen[(neighbour[0], neighbour[1])] < neighbour[2]):
                        # Check that we've not already been here in this exact state, but with a shorter length
                        # Even though we perform this check when queueing a state, it might be possible
                        # for the length to be beaten by an earlier queued state, and so we check in both places.
                        queue.append(neighbour)
                        seen[(neighbour[0], neighbour[1])] = neighbour[2]

            # Ensure that the queue is sorted, such that the smallest length is at the end of the list
            # This lets us implement Dijkstra's algorithm (always considering the smallest total cost)
            # while also not needing to use a deque (popping from the end) as deques can't be sorted in-place
            queue.sort(reverse=True, key=lambda state: state[2])

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The least heat loss that can be incurred is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["2413432311323",
                                       "3215453535623",
                                       "3255245654254",
                                       "3446585845452",
                                       "4546657867536",
                                       "1438598798454",
                                       "4457876987766",
                                       "3637877979653",
                                       "4654967986887",
                                       "4564679986453",
                                       "1224686865563",
                                       "2546548887735",
                                       "4322674655533"]), 94)

    def test_ex2(self):
        return self.assertEqual(solve(["111111111111",
                                       "999999999991",
                                       "999999999991",
                                       "999999999991",
                                       "999999999991"]), 71)

run(main)
