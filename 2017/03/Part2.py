#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import unittest

grid = {(0, 0): 1}
def get_grid(x, y):
    global grid

    try:
        to_return = grid[(x,y)]
        return to_return
    except:
        grid[(x,y)] = 0
        return grid[(x,y)]

def solve(puzzle_input):
    global grid

    x = y = 0

    max_coord = 0
    first_stage_0 = False
    last_calculated = 1

    stage = 3 #0 is moving up, 1 left, 2 down and 3 right
    while last_calculated < puzzle_input:
        if stage == 0:
            if first_stage_0:
                max_coord += 1
                y += 1
                first_stage_0 = False
            if y == -max_coord:
                stage = 1
            else:
                y -= 1
        elif stage == 1:
            if x == -max_coord:
                stage = 2
            else:
                x -= 1
        elif stage == 2:
            if y == max_coord:
                stage = 3
            else:
                y += 1
        elif stage == 3:
            if x == max_coord:
                stage = 0
                first_stage_0 = True
            x += 1

        grid[(x,y)] = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    grid[(x,y)] += get_grid(x+i,y+j)
        last_calculated = grid[(x,y)]

    return grid[(x,y)]

def main():
    f = open("puzzle_input.txt")
    puzzle_input = int(f.read()[:-1])
    f.close()

    value = solve(puzzle_input)

    print("The first value written that is greater than the puzzle input is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    def setUp(self):
        global grid
        grid = {(0, 0): 1}
        solve(5)

    def test_ex1(self):
        self.assertEqual(get_grid(0, 0), 1)

    def test_ex2(self):
        self.assertEqual(get_grid(1, 0), 1)

    def test_ex3(self):
        self.assertEqual(get_grid(1, -1), 2)

    def test_ex4(self):
        self.assertEqual(get_grid(0, -1), 4)

    def test_ex5(self):
        self.assertEqual(get_grid(-1, -1), 5)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
