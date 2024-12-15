#!/usr/bin/env python3

#Advent of Code
#2024 Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import dropwhile, takewhile
from typing import Iterable, Self

def solve(puzzle_input: list[str]) -> int:
    class Object:
        warehouse_ref: "Warehouse"
        x: int
        y: int

        def __init__(self: Self, warehouse_ref: "Warehouse", x: int, y: int) -> None:
            self.warehouse_ref = warehouse_ref
            self.x = x
            self.y = y

        def push(self: Self, from_loc: tuple[int, int]) -> bool:
            return False

        def gps(self: Self) -> int:
            return (100 * self.y) + self.x

    class Wall(Object):
        # Walls cannot be pushed under any circumstances
        def push(self: Self, from_loc: tuple[int, int]) -> bool:
            return False

    class Box(Object):
        # Boxes can only be pushed if the space to move in to is empty or pushable
        def push(self: Self, from_loc: tuple[int, int]) -> bool:
            dx: int = self.x - from_loc[0]
            dy: int = self.y - from_loc[1]

            if self.warehouse_ref.can_push((self.x, self.y), (self.x + dx, self.y + dy)):
                self.warehouse_ref.move((self.x, self.y), (self.x + dx, self.y + dy))
                return True
            else:
                return False

    class Robot(Object):
        # It doesn't make sense for the robot to be pushed
        def push(self: Self, from_loc: tuple[int, int]) -> bool:
            raise RuntimeError("Tried to push the robot")

        def follow_instruction(self: Self, direction: str) -> None:
            match direction:
                case "^":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x, self.y - 1)):
                        self.warehouse_ref.move((self.x, self.y), (self.x, self.y - 1))
                case ">":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x + 1, self.y)):
                        self.warehouse_ref.move((self.x, self.y), (self.x + 1, self.y))
                case "v":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x, self.y + 1)):
                        self.warehouse_ref.move((self.x, self.y), (self.x, self.y + 1))
                case "<":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x - 1, self.y)):
                        self.warehouse_ref.move((self.x, self.y), (self.x - 1, self.y))

    class Warehouse:
        objects: dict[tuple[int, int], "Object"]
        robot: Robot

        def __init__(self: Self, warehouse_map: Iterable[str]) -> None:
            self.objects = {}
            for y, row in enumerate(warehouse_map):
                for x, col in enumerate(row):
                    match col:
                        case "#":
                            self.objects[(x, y)] = Wall(self, x, y)
                        case "O":
                            self.objects[(x, y)] = Box(self, x, y)
                        case "@":
                            self.objects[(x, y)] = self.robot = Robot(self, x, y)

        def can_push(self: Self, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> bool:
            if to_loc in self.objects:
                return self.objects[to_loc].push(from_loc)
            else:
                return True

        def move(self: Self, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> None:
            self.objects[to_loc] = self.objects[from_loc]
            self.objects[to_loc].x = to_loc[0]
            self.objects[to_loc].y = to_loc[1]
            del self.objects[from_loc]

    warehouse: Warehouse = Warehouse(takewhile(len, puzzle_input))
    for instruction in "".join(dropwhile(lambda line: len(line) == 0 or not line[0] in "^>v<", puzzle_input)):
        warehouse.robot.follow_instruction(instruction)

    return sum(o.gps() for o in warehouse.objects.values() if isinstance(o, Box))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of all boxes' final GPS coordinates is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["##########",
                                       "#..O..O.O#",
                                       "#......O.#",
                                       "#.OO..O.O#",
                                       "#..O@..O.#",
                                       "#O#..O...#",
                                       "#O..O..O.#",
                                       "#.OO.O.OO#",
                                       "#....O...#",
                                       "##########",
                                       "",
                                       "<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^",
                                       "vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v",
                                       "><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<",
                                       "<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^",
                                       "^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><",
                                       "^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^",
                                       ">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^",
                                       "<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>",
                                       "^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>",
                                       "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"]), 10092)

    def test_ex2(self):
        return self.assertEqual(solve(["########",
                                       "#..O.O.#",
                                       "##@.O..#",
                                       "#...O..#",
                                       "#.#.O..#",
                                       "#...O..#",
                                       "#......#",
                                       "########",
                                       "",
                                       "<^^>>>vv<v>>v<<"]), 2028)

run(main)
