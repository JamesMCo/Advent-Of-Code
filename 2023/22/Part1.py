#!/usr/bin/env python3

#Advent of Code
#2023 Day 22, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
import re

def solve(puzzle_input: list[str]) -> int:
    bricks: list["Brick"] = []
    brick_tops_by_height: defaultdict[int, list["Brick"]] = defaultdict(list)

    class Brick:
        x: int
        y: int
        z: int
        width: int
        depth: int
        height: int

        _dependencies: list["Brick"] | None
        solely_relied_upon: bool

        brick_pattern: re.Pattern = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

        def __init__(self: "Brick", brick_description: str) -> None:
            x1, y1, z1, x2, y2, z2 = map(int, self.brick_pattern.match(brick_description).groups())

            self.x = min(x1, x2)
            self.y = min(y1, y2)
            self.z = min(z1, z2)

            self.width = abs(x1 - x2) + 1
            self.depth = abs(y1 - y2) + 1
            self.height = abs(z1 - z2) + 1

            self._dependencies = None
            self.solely_relied_upon = False

            bricks.append(self)
            brick_tops_by_height[self.z + self.height - 1].append(self)

        def __str__(self: "Brick") -> str:
            return f"{self.x},{self.y},{self.z}~{self.x+self.width-1},{self.y+self.depth-1},{self.z+self.height-1}"

        @property
        def cubes(self: "Brick") -> int:
            return self.width * self.depth * self.height

        def __lt__(self: "Brick", other: "Brick") -> bool:
            # According to https://docs.python.org/3/library/functions.html#sorted
            # it is sufficient (though not recommended) to
            # only implement __lt__ for sorting.
            return self.z < other.z

        def __contains__(self, coordinate) -> bool:
            return self.x <= coordinate[0] < self.x + self.width and \
                self.y <= coordinate[1] < self.y + self.depth and \
                self.z <= coordinate[2] < self.z + self.height

        def drop(self: "Brick") -> None:
            while True:
                if self.z == 1:
                    # Can't fall through the floor
                    return

                for x in range(self.x, self.x + self.width):
                    for y in range(self.y, self.y + self.depth):
                        if any((x, y, self.z - 1) in lower_brick for lower_brick in brick_tops_by_height[self.z - 1]):
                            # Can't fall through another brick
                            return

                # Nothing below this brick, so drop one space
                brick_tops_by_height[self.z + self.height - 1].remove(self)
                self.z -= 1
                brick_tops_by_height[self.z + self.height - 1].append(self)

        @property
        def dependencies(self: "Brick") -> list["Brick"]:
            if not self._dependencies:
                lower_bricks: set["Brick"] = set()
                for lower_brick in brick_tops_by_height[self.z - 1]:
                    is_dependency = False
                    for x in range(self.x, self.x + self.width):
                        for y in range(self.y, self.y + self.depth):
                            if (x, y, self.z - 1) in lower_brick:
                                lower_bricks.add(lower_brick)
                                is_dependency = True
                                break
                        if is_dependency:
                            break
                self._dependencies = list(lower_bricks)
            return self._dependencies

        def alert_sole_dependencies(self: "Brick") -> None:
            if len(self.dependencies) == 1:
                self.dependencies[0].solely_relied_upon = True

    for line in puzzle_input:
        Brick(line)

    for brick in sorted(bricks):
        brick.drop()
        brick.alert_sole_dependencies()

    return len([brick for brick in bricks if not brick.solely_relied_upon])

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of bricks that could safely be chosen to be disintegrated is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1,0,1~1,2,1",
                                       "0,0,2~2,0,2",
                                       "0,2,3~2,2,3",
                                       "0,0,4~0,2,4",
                                       "2,0,5~2,2,5",
                                       "0,1,6~2,1,6",
                                       "1,1,8~1,1,9"]), 5)

run(main)
