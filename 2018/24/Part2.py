#!/usr/bin/env python3

#Advent of Code
#2018 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import typing as t

def solve(puzzle_input):
    class Group:
        units: int
        hit_points: int
        attack_damage: int
        attack_type: str
        initiative: int
        weaknesses: set[str]
        immunities: set[str]

        initial_units: int
        boost: int

        group_pattern: re.Pattern = re.compile(r"(\d+) units? each with (\d+) hit points? (\([^)]+\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)")
        weaknesses_pattern: re.Pattern = re.compile(r"weak to ((?:\w+, )*\w+)[;)]")
        immunities_pattern: re.Pattern = re.compile(r"immune to ((?:\w+, )*\w+)[;)]")

        def __init__(self: t.Self, group_definition: str) -> None:
            parsed_data = self.group_pattern.match(group_definition).groups()

            self.units         = int(parsed_data[0])
            self.hit_points    = int(parsed_data[1])
            self.weaknesses = set()
            self.immunities = set()
            if parsed_data[2] is not None:
                if weaknesses := self.weaknesses_pattern.search(parsed_data[2]):
                    self.weaknesses.update(weaknesses.group(1).split(", "))
                if immunities := self.immunities_pattern.search(parsed_data[2]):
                    self.immunities.update(immunities.group(1).split(", "))
            self.attack_damage = int(parsed_data[3])
            self.attack_type   =     parsed_data[4]
            self.initiative    = int(parsed_data[5])

            self.initial_units = self.units
            self.boost = 0

        def __str__(self: t.Self) -> str:
            return f"{self.units} unit{'' if self.units == 1 else 's'} " +\
                   f"each with {self.hit_points} hit point{'' if self.hit_points == 1 else 's'} " +\
                   ((
                      "(" +
                      (f"weak to {", ".join(self.weaknesses)}" if self.weaknesses else "") +
                      ("; " if self.weaknesses and self.immunities else "") +
                      (f"immune to {", ".join(self.immunities)}" if self.immunities else "") +
                      ") "
                   ) if self.weaknesses or self.immunities else "") +\
                   f"with an attack that does {self.attack_damage} {self.attack_type} damage " +\
                   f"at initiative {self.initiative}"

        @property
        def effective_power(self: t.Self) -> int:
            return self.units * (self.attack_damage + self.boost)

        def damage_query(self: t.Self, attack_damage: int, attack_type: str) -> int:
            if attack_type in self.immunities:
                return 0
            elif attack_type in self.weaknesses:
                return attack_damage * 2
            else:
                return attack_damage

        def target_selection_phase(self: t.Self, remaining_targets: set[t.Self]) -> t.Optional[t.Self]:
            if not remaining_targets:
                return None

            targets = sorted(
                remaining_targets,
                key=lambda g: (
                    g.damage_query(self.effective_power, self.attack_type),
                    g.effective_power,
                    g.initiative
                ),
                reverse=True
            )
            return targets[0] if targets[0].damage_query(self.effective_power, self.attack_type) != 0 else None

        def try_to_attack(self: t.Self, other: t.Self) -> tuple[int, int]:
            if not self.units:
                return 0, 0
            else:
                damage_dealt = other.damage_query(self.effective_power, self.attack_type)
                killed_units = min(other.units, damage_dealt // other.hit_points)
                other.units -= killed_units
                return damage_dealt, killed_units

    class Army:
        name: str
        groups: list[Group]
        armies_dict: dict[str, t.Self]

        def __init__(self: t.Self, armies_dict: dict[str, t.Self], groups: list[str]) -> None:
            self.name = groups[0][:-1]
            self.groups = [Group(group) for group in groups[1:]]

            self.armies = armies_dict
            self.armies[self.name] = self

        def reset(self: t.Self) -> None:
            for group in self.groups:
                group.units = group.initial_units
                group.boost = 0

        def set_boost(self: t.Self, boost_amount: int) -> None:
            for group in self.groups:
                group.boost = boost_amount

        def target_selection_phase(self: t.Self) -> list[tuple[Group, Group]]:
            enemy_army_groups = set([(group for group in army.groups if group.units) for army in self.armies.values() if army.name != self.name][0])
            chosen_targets = []
            for group in sorted((group for group in self.groups if group.units), key=lambda g: (g.effective_power, g.initiative), reverse=True):
                if chosen := group.target_selection_phase(enemy_army_groups):
                    chosen_targets.append((group, chosen))
                    enemy_army_groups.remove(chosen)
            return chosen_targets

        def units_remaining(self: t.Self) -> int:
            return sum(group.units for group in self.groups)

    armies: dict[str, Army] = {}
    army_lines = []
    for line in puzzle_input:
        if line:
            army_lines.append(line)
        else:
            Army(armies, army_lines)
            army_lines = []
    Army(armies, army_lines)

    def try_boost(boost: int) -> t.Optional[int]:
        for a in armies.values():
            a.reset()
        armies["Immune System"].set_boost(boost)

        while all(a.units_remaining() for a in armies.values()):
            # Target Selection Phase
            attacks = []
            for a in armies.values():
                attacks.extend(a.target_selection_phase())

            total_killed = 0
            # Attacking Phase
            for attacker, defender in sorted(attacks, key=lambda ad: ad[0].initiative, reverse=True):
                _, killed = attacker.try_to_attack(defender)
                total_killed += killed
            if total_killed == 0:
                # No units were killed this turn - this won't change in future turns
                # and is therefore a stalemate
                # (insight learned after reading a little on the subreddit while trying to debug part 1)
                return None

        if immune_system_units := armies["Immune System"].units_remaining():
            return immune_system_units

    b = 1
    while True:
        if immune_winning_units := try_boost(b):
            return immune_winning_units
        b += 1

def main():
    puzzle_input = util.read.as_lines()

    units = solve(puzzle_input)

    print("The number of units that the immune system would have after the smallest boost needed for it to win is " + str(units) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["Immune System:",
                                "17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2",
                                "989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3",
                                "",
                                "Infection:",
                                "801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1",
                                "4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"]), 51)

if __name__ == "__main__":
    run(main)
