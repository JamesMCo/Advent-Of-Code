#!/usr/bin/env python3

#Advent of Code
#2022 Day 19, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
from math import ceil, inf
import re

def solve(puzzle_input):
    # This solution includes some optimisations from this reddit post by /u/megamangomuncher
    # https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0ub00e
    # 
    # It was later rewritten using optimisations described in this reddit post by /u/paul_sb76
    # https://www.reddit.com/r/adventofcode/comments/zpy5rm/
    # and the pruning based on best time method described in this reddit comment by /u/DrunkHacker
    # https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0wtmjq/
    # 
    # The next day, I managed to get a working version of this part together, though I'm not entirely
    # sure what about the previous pruning methods were breaking it in the example and the real input.
    # It's working now, though!

    time_limit = 32

    def additional_geodes_if_making_one_robot_per_minute(minutes_remaining):
        n = minutes_remaining - 1
        return int((n*(n+1))/2)

    def worth_making_robot(existing_robot_count, existing_material_count, minutes_remaining, max_material_needed):
        return (existing_robot_count * minutes_remaining) + existing_material_count < minutes_remaining * max_material_needed

    def minutes_to_make_robot(existing_material_a, needed_material_a, material_a_robots, existing_material_b=None, needed_material_b=None, material_b_robots=None):
        def minutes_to_make_robot_single(existing_material, needed_material, robots):
            if needed_material <= existing_material:
                # We already have enough materials to make this robot
                return 1
            elif robots == 0:
                # If there are no robots, and we don't have enough materials, we can't make this robot
                return inf
            else:
                # There aren't enough materials yet, but we have robots, so we will eventually have enough
                return ceil((needed_material - existing_material) / robots) + 1

        minutes_until_a = minutes_to_make_robot_single(existing_material_a, needed_material_a, material_a_robots)
        if any(arg != None for arg in [existing_material_b, needed_material_b, material_b_robots]):
            minutes_until_b = minutes_to_make_robot_single(existing_material_b, needed_material_b, material_b_robots)
            return max(minutes_until_a, minutes_until_b)
        else:
            return minutes_until_a

    def simulate(ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost):
        max_ore_needed = max(ore_cost, clay_cost, obsidian_ore_cost, geode_ore_cost)
        max_clay_needed = obsidian_clay_cost
        max_obsidian_needed = geode_obsidian_cost

        best_at_time = {t: 0 for t in range(time_limit + 1)}
        seen = {}
        to_explore = deque([(time_limit, 0, 0, 0, 0, 1, 0, 0)])

        while to_explore:
            minutes_remaining, inv_ore, inv_clay, inv_obsidian, inv_geode, robots_ore, robots_clay, robots_obsidian = to_explore.popleft()
            seen_key = (inv_ore, inv_clay, inv_obsidian, inv_geode, robots_ore, robots_clay, robots_obsidian)
            if seen_key in seen and seen[seen_key] >= minutes_remaining:
                # Have seen this state at an earlier or equal timestep before
                continue
            best_at_time[minutes_remaining] = max(best_at_time[minutes_remaining], inv_geode)
            seen[seen_key] = minutes_remaining

            # It is always worth trying to make a geode robot (no max needed)
            minutes_to_make_geode_robot = minutes_to_make_robot(inv_ore, geode_ore_cost, robots_ore, inv_obsidian, geode_obsidian_cost, robots_obsidian)
            if minutes_remaining - minutes_to_make_geode_robot > 0:
                # When creating a geode robot, immediately add the geodes it could crack to inv_geode and don't track the number of geode robots directly
                # https://www.reddit.com/r/adventofcode/comments/zpy5rm/comment/j0vk97a/
                to_explore.append((minutes_remaining - minutes_to_make_geode_robot,
                                   inv_ore + (minutes_to_make_geode_robot * robots_ore) - geode_ore_cost,
                                   inv_clay + (minutes_to_make_geode_robot * robots_clay),
                                   inv_obsidian + (minutes_to_make_geode_robot * robots_obsidian) - geode_obsidian_cost,
                                   inv_geode + (minutes_remaining - minutes_to_make_geode_robot),
                                   robots_ore,
                                   robots_clay,
                                   robots_obsidian
                                 ))

            # If it is worth making an obsidian robot, and it is possible in the time remaining, then do so
            if worth_making_robot(robots_obsidian, inv_obsidian, minutes_remaining, max_obsidian_needed):
                minutes_to_make_obsidian_robot = minutes_to_make_robot(inv_ore, obsidian_ore_cost, robots_ore, inv_clay, obsidian_clay_cost, robots_clay)
                if minutes_remaining - minutes_to_make_obsidian_robot > 0:
                    to_explore.append((minutes_remaining - minutes_to_make_obsidian_robot,
                                       inv_ore + (minutes_to_make_obsidian_robot * robots_ore) - obsidian_ore_cost,
                                       inv_clay + (minutes_to_make_obsidian_robot * robots_clay) - obsidian_clay_cost,
                                       inv_obsidian + (minutes_to_make_obsidian_robot * robots_obsidian),
                                       inv_geode,
                                       robots_ore,
                                       robots_clay,
                                       robots_obsidian + 1
                                     ))

            # If it is worth making a clay robot, and it is possible in the time remaining, then do so
            if worth_making_robot(robots_clay, inv_clay, minutes_remaining, max_clay_needed):
                minutes_to_make_clay_robot = minutes_to_make_robot(inv_ore, clay_cost, robots_ore)
                if minutes_remaining - minutes_to_make_clay_robot > 0:
                    to_explore.append((minutes_remaining - minutes_to_make_clay_robot,
                                       inv_ore + (minutes_to_make_clay_robot * robots_ore) - clay_cost,
                                       inv_clay + (minutes_to_make_clay_robot * robots_clay),
                                       inv_obsidian + (minutes_to_make_clay_robot * robots_obsidian),
                                       inv_geode,
                                       robots_ore,
                                       robots_clay + 1,
                                       robots_obsidian
                                     ))

            # If it is worth making an ore robot, and it is possible in the time remaining, then do so
            if worth_making_robot(robots_ore, inv_ore, minutes_remaining, max_ore_needed):
                minutes_to_make_ore_robot = minutes_to_make_robot(inv_ore, ore_cost, robots_ore)
                if minutes_remaining - minutes_to_make_ore_robot > 0:
                    to_explore.append((minutes_remaining - minutes_to_make_ore_robot,
                                       inv_ore + (minutes_to_make_ore_robot * robots_ore) - ore_cost,
                                       inv_clay + (minutes_to_make_ore_robot * robots_clay),
                                       inv_obsidian + (minutes_to_make_ore_robot * robots_obsidian),
                                       inv_geode,
                                       robots_ore + 1,
                                       robots_clay,
                                       robots_obsidian
                                     ))

        return max(x for x in best_at_time.values())

    total_quality = 1
    for line in puzzle_input[:3]:
        blueprint_id, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = [int(x) for x in re.match(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line).groups()]
        max_geodes = simulate(ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost)
        total_quality *= max_geodes

    return total_quality

def main():
    puzzle_input = util.read.as_lines()

    prod_of_maxes = solve(puzzle_input)

    print("The product of the maximum number of geodes collectable by the first three blueprints is " + str(prod_of_maxes) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
                                       "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."]), 56*62)

run(main)
