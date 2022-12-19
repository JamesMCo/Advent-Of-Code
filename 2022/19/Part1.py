#!/usr/bin/env python3

#Advent of Code
#2022 Day 19, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    # This solution includes some optimisations from this reddit post by /u/megamangomuncher
    # https://www.reddit.com/r/adventofcode/comments/zpihwi/comment/j0ub00e

    seen = {}

    def build_options(costs, inv_ore, inv_clay, inv_obsidian):
        # Returns a list of tuples of the number of robots that could be created
        # Each tuple is in the order: ore-collecting, clay-collecting, obsidian-rollecting, geode-cracking, remaining inventory
        ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = costs

        options = []
        if inv_ore >= geode_ore_cost and inv_obsidian >= geode_obsidian_cost:
            # Build a geode-cracking robot
            options.append((0, 0, 0, 1, (inv_ore - geode_ore_cost, inv_clay, inv_obsidian - geode_obsidian_cost)))
        if inv_ore >= obsidian_ore_cost and inv_clay >= obsidian_clay_cost:
            # Build an obsidian-collecting robot
            options.append((0, 0, 1, 0, (inv_ore - obsidian_ore_cost, inv_clay - obsidian_clay_cost, inv_obsidian)))
        if inv_ore >= clay_cost:
            # Build a clay-collecting robot
            options.append((0, 1, 0, 0, (inv_ore - clay_cost, inv_clay, inv_obsidian)))
        if inv_ore >= ore_cost:
            # Build an ore-collecting robot
            options.append((1, 0, 0, 0, (inv_ore - ore_cost, inv_clay, inv_obsidian)))
        # Build nothing
        options.append((0,0,0,0, (inv_ore, inv_clay, inv_obsidian)))

        return options

    def simulate(costs, minute=1,
                 ore_robots=1, clay_robots=0, obsidian_robots=0, geode_robots=0,
                 inv_ore=0, inv_clay=0, inv_obsidian=0, inv_geode=0):
        seen_key = (ore_robots, clay_robots, obsidian_robots, geode_robots, inv_ore, inv_clay, inv_obsidian, inv_geode)
        if seen_key in seen and seen[seen_key] <= minute:
            # Already seen this state earlier or at the same point in the simulation compared to now, so couldn't possibly get more geodes than that.
            # Return 0 so this branch isn't considered.
            return 0

        ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = costs
        # print(f"Simulating minute {minute} with:\n  Ore Robots: {ore_robots}\n  Clay Robots: {clay_robots}\n  Obsidian Robots: {obsidian_robots}\n  Geode Robots: {geode_robots}\n  Inv: {inv_ore} ore, {inv_clay} clay, {inv_obsidian} obsidian, {inv_geode} geodes")

        collected_ore      = ore_robots
        collected_clay     = clay_robots
        collected_obsidian = obsidian_robots
        collected_geode    = geode_robots

        if minute == 24:
            return inv_geode + collected_geode

        max_geodes = inv_geode
        for option in build_options(costs, inv_ore, inv_clay, inv_obsidian):
            # print(f"    Option for building: {option}")
            new_ore_robots, new_clay_robots, new_obsidian_robots, new_geode_robots, new_inv = option
            max_geodes = max(max_geodes,
                             simulate(costs, minute+1,
                                      ore_robots+new_ore_robots, clay_robots+new_clay_robots, obsidian_robots+new_obsidian_robots, geode_robots+new_geode_robots,
                                      new_inv[0]+collected_ore, new_inv[1]+collected_clay, new_inv[2]+collected_obsidian, inv_geode+collected_geode
                                     )
                            )

        seen[seen_key] = minute
        return max_geodes

    total_quality = 0
    for line in puzzle_input:
        seen = {}
        blueprint_id, ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost = [int(x) for x in re.match("Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.", line).groups()]
        max_geodes = simulate((ore_cost, clay_cost, obsidian_ore_cost, obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost))
        total_quality += blueprint_id * max_geodes
        print(f"Blueprint {blueprint_id} can crack a maximum of {max_geodes} geodes")

    return total_quality

def main():
    puzzle_input = util.read.as_lines()

    quality_levels = solve(puzzle_input)

    print("The sum of all quality levels is " + str(quality_levels) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.",
                                       "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."]), 33)

run(main)
