#!/usr/bin/env python3

#Advent of Code
#2018 Day 15, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import colorama, time
from math import inf
from collections import defaultdict

def solve(puzzle_input, actual=True):
    class Cavern:
        def __init__(self):
            self.coords = {}
            self.units  = []

        def register_coord(self, x, y, t):
            self.coords[f"{x},{y}"] = t

        def register_unit(self, unit):
            self.units.append(unit)

        def is_free(self, x, y):
            if self.coords[f"{x},{y}"] == ".":
                return not any(unit.alive and unit.x == x and unit.y == y for unit in self.units)
            return False

        def shortest_path(self, start, goal):
            def straight_line_distance(a, b):
                return ((abs(int(a.split(",")[0]) - int(b.split(",")[0])))**2 + (abs(int(a.split(",")[1]) - int(b.split(",")[1])))**2)**0.5

            # A* Search Algorithm, based on pseudocode from Wikipedia (https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode)
            def reconstruct_path(cameFrom, current):
                total_path = [current]
                while current in cameFrom:
                    current = cameFrom[current]
                    total_path.append(current)
                return total_path

            closedSet = set()

            openSet = set()
            openSet.add(start)
            
            cameFrom = {}
            
            gScore = defaultdict(lambda: inf)
            gScore[start] = 0
            
            fScore = defaultdict(lambda: inf)
            fScore[start] = straight_line_distance(start, goal)

            while len(openSet) != 0:
                current = min([x for x in openSet], key=lambda x: fScore[x])
                if current == goal:
                    return len(reconstruct_path(cameFrom, current)) - 1

                openSet.remove(current)
                closedSet.add(current)

                for neighbour in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbourCoord = f"{int(current.split(',')[0])+neighbour[0]},{int(current.split(',')[1])+neighbour[1]}"
                    if not 0 <= int(neighbourCoord.split(",")[0]) < len(puzzle_input[0]) or not 0 <= int(neighbourCoord.split(",")[1]) < len(puzzle_input):
                        continue
                    if not self.is_free(int(neighbourCoord.split(",")[0]), int(neighbourCoord.split(",")[1])):
                        continue
                    
                    if neighbourCoord in closedSet:
                        continue
                    tentative_gScore = gScore[current] + 1

                    if neighbourCoord not in openSet:
                        openSet.add(neighbourCoord)
                    elif tentative_gScore >= gScore[neighbourCoord]:
                        continue

                    cameFrom[neighbourCoord] = current
                    gScore[neighbourCoord] = tentative_gScore
                    fScore[neighbourCoord] = gScore[neighbourCoord] + straight_line_distance(neighbourCoord, goal)

        def step(self):
            self.units = sorted([unit for unit in self.units if unit.alive], key=lambda u: (u.y, u.x))
            if any(unit.step() for unit in self.units) or any(unit.type == Unit.elf and not unit.alive for unit in self.units):
                return True, sum(unit.hp for unit in self.units if unit.alive)
            return False, 0

    class Unit:
        elf    = 0
        goblin = 1

        def __init__(self, x, y, hp, ap):
            self.x  = x
            self.y  = y
            self.hp = hp
            self.ap = ap

            self.alive = True

        def __lt__(self, other):
            if self.y < other.y:
                return True
            elif self.y > other.y:
                return False
            else:
                if self.x < other.x:
                    return True
                else:
                    return False


        def damage(self, amount):
            self.hp -= amount
            if self.hp <= 0:
                self.alive = False

        def step(self):
            if not self.alive:
                return False

            if not self.in_range():
                target = self.find_target()
                if target == "No reachable targets":
                    return False
                elif target == "No potential targets":
                    return True
                self.move_towards(target)

            if self.in_range():
                self.attack()

            return False

        def find_target(self):
            enemies = [u for u in cavern.units if u.alive and u.type != self.type]
            if len(enemies) == 0:
                return "No potential targets"

            targets = {}
            for unit in enemies:
                for offsetX, offsetY in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= unit.x + offsetX < len(puzzle_input[0]) and 0 <= unit.y + offsetY < len(puzzle_input) and cavern.is_free(unit.x + offsetX, unit.y + offsetY):
                        targets[f"{unit.x+offsetX},{unit.y+offsetY}"] = cavern.shortest_path(f"{self.x},{self.y}", f"{unit.x+offsetX},{unit.y+offsetY}")
            distance_values = [t for t in targets.values() if t != None]
            if len(distance_values) == 0:
                return "No reachable targets"

            nearest = min(distance_values)
            potential = sorted([(int(t.split(",")[0]), int(t.split(",")[1])) for t in targets if targets[t] == nearest], key=lambda x: (x[1], x[0]))
            return f"{potential[0][0]},{potential[0][1]}"

        def move_towards(self, target):
            distances = {}
            for offsetX, offsetY in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if 0 <= self.x + offsetX < len(puzzle_input[0]) and 0 <= self.y + offsetY < len(puzzle_input) and cavern.is_free(self.x + offsetX, self.y + offsetY):
                        distances[f"{self.x+offsetX},{self.y+offsetY}"] = cavern.shortest_path(f"{self.x+offsetX},{self.y+offsetY}", target)
                    else:
                        distances[f"{self.x+offsetX},{self.y+offsetY}"] = inf
            distance_values = [d for d in distances.values() if d != None]
            if len(distance_values) == 0:
                return

            nearest = min(distance_values)
            if 0 <= self.y-1 < len(puzzle_input) and cavern.is_free(self.x,self.y-1) and distances[f"{self.x},{self.y-1}"] == nearest:
                self.move(0, -1)
            elif 0 <= self.x-1 < len(puzzle_input[0]) and cavern.is_free(self.x-1,self.y) and distances[f"{self.x-1},{self.y}"] == nearest:
                self.move(-1, 0)
            elif 0 <= self.x+1 < len(puzzle_input[1]) and cavern.is_free(self.x+1,self.y) and distances[f"{self.x+1},{self.y}"] == nearest:
                self.move(1, 0)
            elif 0 <= self.y+1 < len(puzzle_input) and cavern.is_free(self.x,self.y+1) and distances[f"{self.x},{self.y+1}"] == nearest:
                self.move(0, 1)

        def move(self, x, y):
            self.x += x
            self.y += y

        def in_range(self):
            enemies = [u for u in cavern.units if u.alive and u.type != self.type]
            for unit in enemies:
                if abs(self.x - unit.x) + abs(self.y - unit.y) == 1:
                    return True
            return False

        def attack(self):
            enemies = [u for u in cavern.units if u.alive and u.type != self.type]
            targets = []
            for unit in enemies:
                if abs(self.x - unit.x) + abs(self.y - unit.y) == 1:
                    targets.append(unit)
            targets.sort(key=lambda u: (u.hp, u.y, u.x))

            targets[0].damage(self.ap)


    class Elf(Unit):
        def __init__(self, x, y, ap):
            Unit.__init__(self, x, y, 200, ap)
            self.type = Unit.elf

    class Goblin(Unit):
        def __init__(self, x, y):
            Unit.__init__(self, x, y, 200, 3)
            self.type = Unit.goblin

    initial_elf_count = "".join(puzzle_input).count("E")
    ap = 4
    if actual:
        print("\n(Note: The following lines are in place to avoid timing out the Travis build)")

    while True:
        start = time.time()

        cavern = Cavern()
        for y, row in enumerate(puzzle_input):
            for x, col in enumerate(row):
                if col in "#.":
                    cavern.register_coord(x, y, col)
                else:
                    cavern.register_coord(x, y, ".")
                    if col == "E":
                        cavern.register_unit(Elf(x, y, ap))
                    else:
                        cavern.register_unit(Goblin(x, y))

        rounds = 0
        while True:
            terminated, outcome = cavern.step()
            if terminated:
                break
            rounds += 1

        end = time.time()
        duration = str(round(end - start, 3))
        duration += "0" * (3 - len(duration.split(".")[1]))
        if sum(1 for u in cavern.units if u.alive and u.type == Unit.elf) == initial_elf_count:
            if actual:
                print(f"{colorama.Fore.CYAN}Tested AP of {colorama.Fore.YELLOW}{ap}{colorama.Fore.CYAN} in {colorama.Fore.GREEN}{duration}s{colorama.Fore.CYAN} - it was {colorama.Fore.GREEN}correct{colorama.Fore.CYAN}.{colorama.Fore.RESET}")
            return rounds * outcome
        else:
            if actual:
                print(f"{colorama.Fore.CYAN}Tested AP of {colorama.Fore.YELLOW}{ap}{colorama.Fore.CYAN} in {colorama.Fore.GREEN}{duration}s{colorama.Fore.CYAN} - it was {colorama.Fore.RED}incorrect{colorama.Fore.CYAN}.{colorama.Fore.RESET}")
            ap += 1

def main():
    puzzle_input = util.read.as_lines()

    outcome = solve(puzzle_input)

    print("The outcome of the battle is " + str(outcome) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["#######",
                                "#.G...#",
                                "#...EG#",
                                "#.#.#G#",
                                "#..G#E#",
                                "#.....#",
                                "#######"], False), 4988)
        
    def test_ex2(self):
        self.assertEqual(solve(["#######",
                                "#E..EG#",
                                "#.#G.E#",
                                "#E.##E#",
                                "#G..#.#",
                                "#..E#.#",
                                "#######"], False), 31284)
        
    def test_ex3(self):
        self.assertEqual(solve(["#######",
                                "#E.G#.#",
                                "#.#G..#",
                                "#G.#.G#",
                                "#G..#.#",
                                "#...E.#",
                                "#######"], False), 3478)
        
    def test_ex4(self):
        self.assertEqual(solve(["#######",
                                "#.E...#",
                                "#.#..G#",
                                "#.###.#",
                                "#E#G#G#",
                                "#...#G#",
                                "#######"], False), 6474)
        
    def test_ex5(self):
        self.assertEqual(solve(["#########",
                                "#G......#",
                                "#.E.#...#",
                                "#..##..G#",
                                "#...##..#",
                                "#...#...#",
                                "#.G...G.#",
                                "#.....G.#",
                                "#########"], False), 1140)

if __name__ == "__main__":
    run(main)
