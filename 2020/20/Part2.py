#!/usr/bin/env python3

#Advent of Code
#2020 Day 20, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def consume_section():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(line)
        return output
      
    def consume_tile():
        raw = consume_section()
        tile_id = int(raw[0].split()[1][:-1])
        return (tile_id, raw[1:])

    def side_to_hash(side):
        b = side.replace(".", "0").replace("#", "1")
        return int(b, 2)

    def rotate_tile(tile):
        output = []
        for y in range(len(tile) - 1, -1, -1):
            output.append("")
            for x in range(len(tile[0])):
                output[-1] += tile[x][y]
        return output

    def tile_transforms(tile):
        yield tile
        for i in range(3):
            tile = rotate_tile(tile)
            yield tile
        tile = [row[::-1] for row in tile]
        yield tile
        for i in range(3):
            tile = rotate_tile(tile)
            yield tile        

    def find_monster(img, x, y):
        monster_positions = [(18, 0),
                             (0, 1), (5, 1), (6, 1), (11, 1), (12, 1), (17, 1), (18, 1), (19, 1),
                             (1, 2), (4, 2), (7, 2), (10, 2), (13, 2), (16, 2)]

        for dx, dy in monster_positions:
            if img[y + dy][x + dx] != "#":
                return False
        # Found a monster
        for dx, dy in monster_positions:
            img[y + dy] = img[y + dy][:x + dx] + "O" + img[y + dy][x + dx + 1:]
        return True

    tiles = {}
    while puzzle_input:
        t = consume_tile()
        tiles[t[0]] = t[1]

    width = int(len(tiles)**0.5)
    def fit(grid=[]):
        if len(grid) == 0:
            for t in tiles:
                for r in tile_transforms(tiles[t]):
                    result = fit([(t, r)])
                    if result != False:
                        return result
            return False
        if len(grid) == len(tiles):
            return grid

        has_left = len(grid) % width != 0
        if has_left:
            left = grid[-1]
        has_top  = len(grid) > width
        if has_top:
            top = grid[-width]

        for t in tiles:
            if t in [x[0] for x in grid]:
                continue
            for r in tile_transforms(tiles[t]):
                if has_left:
                    left_hash = side_to_hash("".join(x[-1] for x in left[1]))
                    if left_hash != side_to_hash("".join(x[0] for x in r)):
                        continue
                if has_top:
                    top_hash = side_to_hash(top[1][-1])
                    if top_hash != side_to_hash(r[0]):
                        continue
                result = fit(grid + [(t, r)])
                if result != False:
                    return result
        return False

    grid = fit()

    rawimage = []
    for tile_row in range(0, len(grid), width):
        for sub_row in range(1, len(grid[0][1])-1):
            rawimage.append("".join(tile[1][sub_row][1:-1] for tile in grid[tile_row:tile_row+width]))

    for img in tile_transforms(rawimage):
        final = False
        for y in range(len(rawimage) - 2):
            for x in range(len(rawimage[0]) - 19):
                final |= find_monster(img, x, y)
        if final: break

    return "".join(img).count("#")

def main():
    puzzle_input = util.read.as_lines()

    not_monsters = solve(puzzle_input)

    print("The number of # that are not part of a monster is " + str(not_monsters) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Tile 2311:",
                                       "..##.#..#.",
                                       "##..#.....",
                                       "#...##..#.",
                                       "####.#...#",
                                       "##.##.###.",
                                       "##...#.###",
                                       ".#.#.#..##",
                                       "..#....#..",
                                       "###...#.#.",
                                       "..###..###",
                                       "",
                                       "Tile 1951:",
                                       "#.##...##.",
                                       "#.####...#",
                                       ".....#..##",
                                       "#...######",
                                       ".##.#....#",
                                       ".###.#####",
                                       "###.##.##.",
                                       ".###....#.",
                                       "..#.#..#.#",
                                       "#...##.#..",
                                       "",
                                       "Tile 1171:",
                                       "####...##.",
                                       "#..##.#..#",
                                       "##.#..#.#.",
                                       ".###.####.",
                                       "..###.####",
                                       ".##....##.",
                                       ".#...####.",
                                       "#.##.####.",
                                       "####..#...",
                                       ".....##...",
                                       "",
                                       "Tile 1427:",
                                       "###.##.#..",
                                       ".#..#.##..",
                                       ".#.##.#..#",
                                       "#.#.#.##.#",
                                       "....#...##",
                                       "...##..##.",
                                       "...#.#####",
                                       ".#.####.#.",
                                       "..#..###.#",
                                       "..##.#..#.",
                                       "",
                                       "Tile 1489:",
                                       "##.#.#....",
                                       "..##...#..",
                                       ".##..##...",
                                       "..#...#...",
                                       "#####...#.",
                                       "#..#.#.#.#",
                                       "...#.#.#..",
                                       "##.#...##.",
                                       "..##.##.##",
                                       "###.##.#..",
                                       "",
                                       "Tile 2473:",
                                       "#....####.",
                                       "#..#.##...",
                                       "#.##..#...",
                                       "######.#.#",
                                       ".#...#.#.#",
                                       ".#########",
                                       ".###.#..#.",
                                       "########.#",
                                       "##...##.#.",
                                       "..###.#.#.",
                                       "",
                                       "Tile 2971:",
                                       "..#.#....#",
                                       "#...###...",
                                       "#.#.###...",
                                       "##.##..#..",
                                       ".#####..##",
                                       ".#..####.#",
                                       "#..#.#..#.",
                                       "..####.###",
                                       "..#.#.###.",
                                       "...#.#.#.#",
                                       "",
                                       "Tile 2729:",
                                       "...#.#.#.#",
                                       "####.#....",
                                       "..#.#.....",
                                       "....#..#.#",
                                       ".##..##.#.",
                                       ".#.####...",
                                       "####.#.#..",
                                       "##.####...",
                                       "##..#.##..",
                                       "#.##...##.",
                                       "",
                                       "Tile 3079:",
                                       "#.#.#####.",
                                       ".#..######",
                                       "..#.......",
                                       "######....",
                                       "####.#..#.",
                                       ".#...#.##.",
                                       "#.#####.##",
                                       "..#.###...",
                                       "..#.......",
                                       "..#.###..."]), 273)

run(main)
