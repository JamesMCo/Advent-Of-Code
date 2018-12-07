#!/usr/bin/env python3

#Advent of Code
#Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input, constant_additional_time=60, workers=5):
    steps = {}
    letters = set()
    for step in puzzle_input:
        requirement = step.split()[1]
        after       = step.split()[7]

        letters.add(requirement)
        letters.add(after)

        if after not in steps:
            steps[after]  = requirement
        else:
            steps[after] += requirement

    done = ""
    working = []
    timer = 0

    while len(done) != len(letters):
        while len(working) != workers:
            options = sorted([x for x in letters if x not in steps and x not in [y[0] for y in working] and x not in done])
            if len(options) == 0:
                break

            chosen  = options[0]
            working.append([chosen, constant_additional_time + ord(chosen)-64])

        finished = []
        timer += 1
        for s in range(len(working)):
            if working[s][1] == 1:
                finished.append(s)
                done += working[s][0]
            else:
                working[s][1] -= 1

        if len(finished) > 0:
            to_remove = []
            finished_letters = [working[s][0] for s in finished]

            for s in steps:
                for l in finished_letters:
                    steps[s] = steps[s].replace(l, "")
                if len(steps[s]) == 0:
                    to_remove.append(s)
            for t in to_remove:
                del steps[t]

            for s in sorted(finished, reverse=True):
                working.pop(s)

    return timer

        

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read().strip().split("\n")
    f.close()

    order = solve(puzzle_input)

    print("The order to complete the steps is " + str(order) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["Step C must be finished before step A can begin.",
                                "Step C must be finished before step F can begin.",
                                "Step A must be finished before step B can begin.",
                                "Step A must be finished before step D can begin.",
                                "Step B must be finished before step E can begin.",
                                "Step D must be finished before step E can begin.",
                                "Step F must be finished before step E can begin."], 0, 2), 15)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        start = time.time()
        main()
        end = time.time()
        duration = str(round(end - start, 3))
        duration += "0" * (3 - len(duration.split(".")[1]))
        print(f"{colorama.Fore.CYAN}Solution found in {colorama.Fore.GREEN}{duration}s{colorama.Fore.CYAN}.{colorama.Fore.RESET}")
        exit(0)
    else:
        exit(1)
