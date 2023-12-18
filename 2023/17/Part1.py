#!/usr/bin/env python3

#Advent of Code
#2023 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from dataclasses import dataclass, field
from queue import PriorityQueue

def solve(puzzle_input: list[str]) -> int:
    puzzle_input: list[list[int]] = [[int(n) for n in line] for line in puzzle_input]
    target: tuple[int, int] = (len(puzzle_input[0]) - 1, len(puzzle_input) - 1)

    def in_bounds(x: int, y: int) -> bool:
        return 0 <= x <= target[0] and 0 <= y <= target[1]

    @dataclass(order=True)
    class State:
        coord: tuple[int, int] = field(compare=False)
        direction: str = field(compare=False)
        length: int

    # My original approach was to perform a BFS,
    # tracking how many steps in a given direction
    # had been taken. There were some steps to
    # prune the search space:
    #
    # - Don't consider a state if it has already
    #   been reached with a shorter total length
    # - Don't consider a state if that location
    #   has already been reached, but with fewer
    #   steps in a given direction
    #
    # Though this found the solution to the example
    # in <1s, I ended stopping the puzzle input after
    # something like an hour. After some brief skimming
    # of discussions on reddit, I ended up implementing
    # the following improvements:
    #
    # - From a location, queue all possible movements
    #   from that location. i.e. turn left for 1, 2,
    #   and 3 steps, and turn right for 1, 2, and 3
    #   steps. Don't consider going forwards (because
    #   that state will already be considered by the
    #   state that led you here going 1 further if it
    #   was able to do so) or, of course, reversing.
    # - Use Dijkstra's algorithm rather than a
    #   standard BFS by sorting the queue and considering
    #   the state with the shortest total length. This
    #   also means that, once you see the target once,
    #   then that is the shortest length to reach the target.
    #
    # After the fact, I refactored both parts to use Python's
    # queue.PriorityQueue rather than sorting the list each time.
    # The PriorityQueue uses a heap internally to always return
    # the item with the lowest priority (i.e. shortest length).
    # One downside is that you can't iterate over the contents
    # to see if the state you are about to queue is already queued,
    # and so I also track the contents of the queue with a set.

    queue: PriorityQueue[State] = PriorityQueue()
    queue.put_nowait(State((0, 0), "initial_state", 0))
    queue_set: set[tuple[tuple[int, int], str, int]] = {((0, 0), "initial_state", 0)}
    seen: dict[tuple[tuple[int, int], str], int] = {}
    while not queue.empty():
        state = queue.get_nowait()
        queue_set.remove((state.coord, state.direction, state.length))
        coord, direction, length = state.coord, state.direction, state.length
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

            for steps in range(1, 4):
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
                if neighbour not in queue_set:
                    if not ((neighbour[0], neighbour[1]) in seen and seen[(neighbour[0], neighbour[1])] < neighbour[2]):
                        # Check that we've not already been here in this exact state, but with a shorter length
                        # Even though we perform this check when queueing a state, it might be possible
                        # for the length to be beaten by an earlier queued state, and so we check in both places.
                        queue.put_nowait(State(*neighbour))
                        queue_set.add(neighbour)
                        seen[(neighbour[0], neighbour[1])] = neighbour[2]

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
                                       "4322674655533"]), 102)

run(main)
