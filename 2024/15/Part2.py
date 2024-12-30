#!/usr/bin/env python3

#Advent of Code
#2024 Day 15, Part 2
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

        def can_push(self: Self, from_loc: tuple[int, int]) -> bool:
            return False

        def push(self: Self, from_loc: tuple[int, int]) -> None:
            pass

        def gps(self: Self) -> int:
            return (100 * self.y) + self.x

    class Wall(Object):
        # Walls cannot be pushed under any circumstances
        def can_push(self: Self, from_loc: tuple[int, int]) -> bool:
            return False

    class Box(Object):
        is_extension: bool

        def __init__(self: Self, warehouse_ref: "Warehouse", x: int, y: int, is_extension: bool) -> None:
            super().__init__(warehouse_ref, x, y)
            self.is_extension = is_extension

        # Boxes can only be pushed if the spaces to move in to are empty or pushable
        def can_push(self: Self, from_loc: tuple[int, int]) -> bool:
            dx: int = self.x - from_loc[0]
            dy: int = self.y - from_loc[1]

            if dy != 0:
                if self.is_extension:
                    # Delegate vertical movement to non-extension box
                    return self.warehouse_ref.objects[(self.x - 1, self.y)].can_push((from_loc[0] - 1, from_loc[1]))
                else:
                    # Otherwise, check whether pushing is possible for both
                    # the non-extension and extension boxes
                    return self.warehouse_ref.can_push((self.x, self.y), (self.x, self.y + dy))\
                       and self.warehouse_ref.can_push((self.x + 1, self.y), (self.x + 1, self.y + dy))
            else:
                # Horizontal movement passes through the box and extension box
                # as if they were two separate boxes
                return self.warehouse_ref.can_push((self.x, self.y), (self.x + dx, self.y))

        def push(self: Self, from_loc: tuple[int, int]) -> None:
            dx: int = self.x - from_loc[0]
            dy: int = self.y - from_loc[1]

            if dy != 0:
                if self.is_extension:
                    return self.warehouse_ref.objects[(self.x - 1, self.y)].push((from_loc[0] - 1, from_loc[1]))
                else:
                    return self.warehouse_ref.push((self.x, self.y), (self.x, self.y + dy))\
                       and self.warehouse_ref.push((self.x + 1, self.y), (self.x + 1, self.y + dy))
            else:
                self.warehouse_ref.push((self.x, self.y), (self.x + dx, self.y))

    class Robot(Object):
        # It doesn't make sense for the robot to be pushed
        def can_push(self: Self, from_loc: tuple[int, int]) -> bool:
            raise RuntimeError("Tried to test whether we can push the robot")

        # It still doesn't make sense for the robot to be pushed
        def push(self: Self, from_loc: tuple[int, int]) -> None:
            raise RuntimeError("Tried to push the robot")

        def follow_instruction(self: Self, direction: str) -> None:
            match direction:
                case "^":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x, self.y - 1)):
                        self.warehouse_ref.push((self.x, self.y), (self.x, self.y - 1))
                case ">":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x + 1, self.y)):
                        self.warehouse_ref.push((self.x, self.y), (self.x + 1, self.y))
                case "v":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x, self.y + 1)):
                        self.warehouse_ref.push((self.x, self.y), (self.x, self.y + 1))
                case "<":
                    if self.warehouse_ref.can_push((self.x, self.y), (self.x - 1, self.y)):
                        self.warehouse_ref.push((self.x, self.y), (self.x - 1, self.y))

    class Warehouse:
        objects: dict[tuple[int, int], "Object"]
        robot: Robot

        def __init__(self: Self, warehouse_map: Iterable[str]) -> None:
            self.objects = {}
            for y, row in enumerate(warehouse_map):
                for x, col in enumerate(row):
                    match col:
                        case "#":
                            self.objects[(x * 2, y)] = Wall(self, x * 2, y)
                            self.objects[((x * 2) + 1, y)] = Wall(self, (x * 2) + 1, y)
                        case "O":
                            self.objects[(x * 2, y)] = Box(self, x * 2, y, False)
                            self.objects[((x * 2) + 1, y)] = Box(self, (x * 2) + 1, y, True)
                        case "@":
                            self.objects[(x * 2, y)] = self.robot = Robot(self, x * 2, y)

        def can_push(self: Self, from_loc: tuple[int, int], to_loc: tuple[int, int]) -> bool:
            if to_loc in self.objects:
                return self.objects[to_loc].can_push(from_loc)
            else:
                return True

        def push(self: Self, from_loc: tuple[int, int], to_loc: tuple[int, int], allow_extension_push: bool = False) -> None:
            if from_loc[1] != to_loc[1] and isinstance(self.objects[from_loc], Box) and self.objects[from_loc].is_extension and not allow_extension_push:
                # Delegate pushing a box extension to the non-extension when pushing vertically
                return self.push((from_loc[0] - 1, from_loc[1]), (to_loc[0] - 1, to_loc[1]))

            if to_loc in self.objects:
                self.objects[to_loc].push(from_loc)
            self.objects[to_loc] = self.objects[from_loc]
            self.objects[to_loc].x = to_loc[0]
            self.objects[to_loc].y = to_loc[1]
            del self.objects[from_loc]

            if from_loc[1] != to_loc[1] and isinstance(self.objects[to_loc], Box) and not self.objects[to_loc].is_extension:
                # If we're a non-extension box, we need to push the extension when pushing vertically
                self.push((from_loc[0] + 1, from_loc[1]), (to_loc[0] + 1, to_loc[1]), allow_extension_push=True)

    warehouse: Warehouse = Warehouse(takewhile(len, puzzle_input))
    for instruction in "".join(dropwhile(lambda line: len(line) == 0 or not line[0] in "^>v<", puzzle_input)):
        warehouse.robot.follow_instruction(instruction)

    return sum(o.gps() for o in warehouse.objects.values() if isinstance(o, Box) and not o.is_extension)

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
                                       "v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"]), 9021)

if __name__ == "__main__":
    run(main)
