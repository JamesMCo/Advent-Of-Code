#!/usr/bin/env python3

#Advent of Code
#2023 Day 20, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
from math import lcm
import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    modules: dict[str, "Module"] = {}
    pulse_queue: deque[tuple["Module", "Module", bool]] = deque()

    class Module:
        name: str
        _output_names: list[str]

        inputs: list[t.Self]
        outputs: list[t.Self]

        module_pattern: re.Pattern = re.compile(r"[%&]?(\w+) -> (.*)")

        def __init__(self: t.Self, module_description: str) -> None:
            self.name, outputs = self.module_pattern.match(module_description).groups()
            self._output_names = outputs.split(", ")

            self.inputs = []
            self.outputs = []

            modules[self.name] = self

        def __str__(self: t.Self) -> str:
            return f"{self.name}: Module"

        def register_input(self: t.Self, other: t.Self) -> None:
            self.inputs.append(other)

        def register_outputs(self: t.Self) -> None:
            for output_name in self._output_names:
                output: t.Self = modules[output_name] if output_name in modules else Module(f"{output_name} -> ")
                self.outputs.append(output)
                output.register_input(self)

        def receive_pulse(self: t.Self, module: t.Self, pulse_is_high: bool) -> None:
            # Untyped module just receives pulses, doesn't pass any on
            pass

    class FlipFlopModule(Module):
        state: bool

        def __init__(self: t.Self, module_description: str) -> None:
            super().__init__(module_description)
            self.state = False

        @t.override
        def __str__(self: t.Self) -> str:
            return f"{self.name}: Flip-flop ({"on" if self.state else "off"})"

        @t.override
        def receive_pulse(self: t.Self, module: Module, pulse_is_high: bool) -> None:
            if pulse_is_high:
                # High pulses are ignored
                pass
            else:
                # Low pulses flip the state and send a pulse (high if now on, low if now off)
                self.state = not self.state
                for module in self.outputs:
                    pulse_queue.append((self, module, self.state))

    class ConjunctionModule(Module):
        last_received: dict[str, bool]

        def __init__(self: t.Self, module_description: str) -> None:
            super().__init__(module_description)
            self.last_received = {}

        @t.override
        def __str__(self: t.Self) -> str:
            return f"{self.name}: Conjunction ({self.last_received})"

        @t.override
        def register_input(self: t.Self, other: t.Self) -> None:
            self.inputs.append(other)
            self.last_received[other.name] = False

        @t.override
        def receive_pulse(self: t.Self, module: Module, pulse_is_high: bool) -> None:
            self.last_received[module.name] = pulse_is_high
            if all(self.last_received.values()):
                # If all remembered inputs are high pulses, send a low pulse
                for module in self.outputs:
                    pulse_queue.append((self, module, False))
            else:
                # If all remembered inputs are not high pulses, send a high pulse
                for module in self.outputs:
                    pulse_queue.append((self, module, True))

    class BroadcastModule(Module):
        @t.override
        def receive_pulse(self: t.Self, module: Module, pulse_is_high: bool) -> None:
            # Rebroadcast all incoming pulses to outputs unchanged
            for module in self.outputs:
                pulse_queue.append((self, module, pulse_is_high))

        @t.override
        def __str__(self: t.Self) -> str:
            return f"{self.name}: Broadcast"

    for line in puzzle_input:
        if line[0] == "%":
            FlipFlopModule(line)
        elif line[0] == "&":
            ConjunctionModule(line)
        elif line.startswith("broadcaster "):
            BroadcastModule(line)
        else:
            Module(line)
    for m in list(modules.values()):
        m.register_outputs()

    # Some observations/notes based on my input (may not generalise to all inputs!)
    #
    # rx's only input is &hp
    # &hp needs all of its inputs to be high
    #
    # &hp's inputs are &sr, &sn, &rf, and &vq
    #
    # After going down a rabbit hole trying to map the connections between modules,
    # I read the general approach that a friend on a Discord server took, which was
    # to look for cycles (like in Day 8).
    #
    # Only going to look for loops in the layer two below the rx module
    # (i.e. the layer of conjunctions feeding in to &hp).

    button = Module("button -> broadcaster")
    button_presses = 0
    module_high_pulses: dict[Module, list[int]] = {m: [] for m in modules["rx"].inputs[0].inputs}
    while True:
        pulse_queue.append((button, modules["broadcaster"], False))
        button_presses += 1

        while pulse_queue:
            from_module: Module
            to_module: Module
            pulse: bool
            from_module, to_module, pulse = pulse_queue.popleft()

            if from_module in module_high_pulses and pulse:
                module_high_pulses[from_module].append(button_presses)

            to_module.receive_pulse(from_module, pulse)

        if all(len(pulses) == 2 for pulses in module_high_pulses.values()):
            # All modules of interest have cycled
            for pulses in module_high_pulses.values():
                length_of_cycle = pulses[1] - pulses[0]
                start_of_cycle = pulses[0]
                if length_of_cycle != start_of_cycle:
                    # This is an assumption I'm making based on my own input
                    # and holds true for it, but I'm not sure if this is a
                    # general property. Therefore, I'm checking for it and
                    # failing on purpose if it doesn't hold, because the
                    # given answer would not be correct.
                    return 0
            # The assumed property holds, meaning all cycles start at 0
            # button presses. Just return the lcm of the cycle lengths.
            return lcm(*[pulses[0] for pulses in module_high_pulses.values()])

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of button presses required to deliver a low pulse to the module named rx is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
