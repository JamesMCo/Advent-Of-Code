#!/usr/bin/env python3

#Advent of Code
#Day 19, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import string, unittest

def solve(puzzle_input):
    steps = 1
    direction = "d"
    cur_x = 0
    cur_y = 0
    prev_x = -1
    prev_y = -1
    max_x = len(puzzle_input[0])
    max_y = len(puzzle_input)

    spaces = "|-+" + string.ascii_uppercase

    while puzzle_input[0][cur_x] != "|":
        cur_x += 1

    while (cur_x, cur_y) != (prev_x, prev_y):
        prev_x, prev_y = cur_x, cur_y

        if direction == "d":
            if cur_y != max_y and puzzle_input[cur_y+1][cur_x] in spaces:
                cur_y += 1
            elif cur_x != max_x and puzzle_input[cur_y][cur_x+1] in spaces:
                cur_x += 1
                direction = "r"
            elif cur_x != 0 and puzzle_input[cur_y][cur_x-1] in spaces:
                cur_x -= 1
                direction = "l"
        elif direction == "u":
            if cur_y != 0 and puzzle_input[cur_y-1][cur_x] in spaces:
                cur_y -= 1
            elif cur_x != max_x and puzzle_input[cur_y][cur_x+1] in spaces:
                cur_x += 1
                direction = "r"
            elif cur_x != 0 and puzzle_input[cur_y][cur_x-1] in spaces:
                cur_x -= 1
                direction = "l"
        elif direction == "l":
            if cur_x != 0 and puzzle_input[cur_y][cur_x-1] in spaces:
                cur_x -= 1
            elif cur_y != max_y and puzzle_input[cur_y+1][cur_x] in spaces:
                cur_y += 1
                direction = "d"
            elif cur_y != 0 and puzzle_input[cur_y-1][cur_x] in spaces:
                cur_y -= 1
                direction = "u"
        elif direction == "r":
            if cur_x != max_x and puzzle_input[cur_y][cur_x+1] in spaces:
                cur_x += 1
            elif cur_y != max_y and puzzle_input[cur_y+1][cur_x] in spaces:
                cur_y += 1
                direction = "d"
            elif cur_y != 0 and puzzle_input[cur_y-1][cur_x] in spaces:
                cur_y -= 1
                direction = "u"
        if (cur_x, cur_y) != (prev_x, prev_y):
            steps += 1

    return steps

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    steps = solve(puzzle_input)

    print("The number of steps taken is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["     |          ",
                                "     |  +--+    ",
                                "     A  |  C    ",
                                " F---|----E|--+ ",
                                "     |  |  |  D ",
                                "     +B-+  +--+ ",
                                "                "]), 38)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
