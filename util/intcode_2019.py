from collections import deque
from enum import IntEnum
from itertools import batched
from util.colour import *
import typing as t

class ParameterMode(IntEnum):
    POSITION = 0
    IMMEDIATE = 1

class Instruction:
    name:   str = ""
    opcode: int = -1
    length: int = -1

    computer:        "IntcodeComputer"
    raw_parameters:  list[int]
    parameter_modes: list[ParameterMode]

    def __init__(self: t.Self, computer: "IntcodeComputer", raw_opcode: int, memory_address: int) -> None:
        self.computer = computer

        self.raw_parameters = list(self.computer.read_memory(memory_address + 1, self.length - 1))
        self.parameter_modes = [ParameterMode(int(mode)) for mode in str(raw_opcode//100).zfill(self.length - 1)[::-1]]

    def get_parameter(self: t.Self, num: int) -> int:
        match self.parameter_modes[num]:
            case ParameterMode.POSITION:  return self.computer.peek_memory(self.raw_parameters[num])
            case ParameterMode.IMMEDIATE: return self.raw_parameters[num]

    def run(self: t.Self):
        raise NotImplementedError()


    _instructions: t.Optional[dict[int, t.Self]] = None
    @classmethod
    def get(cls: t.Self, computer: "IntcodeComputer", memory_address: int) -> t.Self | t.NoReturn:
        if cls._instructions is None:
            cls._instructions = {inst.opcode: inst for inst in cls.__subclasses__()}

        raw_opcode = computer.peek_memory(memory_address)
        return cls._instructions[raw_opcode % 100](computer, raw_opcode, memory_address)

class ADD(Instruction):
    name:   str = "ADD"
    opcode: int = 1
    length: int = 4

    @t.override
    def run(self: t.Self) -> None:
        a   = self.get_parameter(0)
        b   = self.get_parameter(1)
        out = self.raw_parameters[2]
        self.computer.memory[out] = a + b

    def __str__(self: t.Self) -> str:
        a, b, out = self.raw_parameters
        a_mode, b_mode, out_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("ADD")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")} {bright_magenta(f"{out=}")} {magenta(f"({out_mode})")}"

class MUL(Instruction):
    name:   str = "MUL"
    opcode: int = 2
    length: int = 4

    @t.override
    def run(self: t.Self) -> None:
        a   = self.get_parameter(0)
        b   = self.get_parameter(1)
        out = self.raw_parameters[2]
        self.computer.memory[out] = a * b

    def __str__(self: t.Self) -> str:
        a, b, out = self.raw_parameters
        a_mode, b_mode, out_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("MUL")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")} {bright_magenta(f"{out=}")} {magenta(f"({out_mode})")}"

class INP(Instruction):
    name:   str = "INP"
    opcode: int = 3
    length: int = 2

    @t.override
    def run(self: t.Self) -> None:
        out = self.raw_parameters[0]
        self.computer.memory[out] = self.computer.get_input()

    def __str__(self: t.Self) -> str:
        out = self.raw_parameters[0]
        out_mode = self.parameter_modes[0].name
        return f"{yellow("INP")} {bright_magenta(f"{out=}")} {green(f"({out_mode})")}"

class OUT(Instruction):
    name:   str = "OUT"
    opcode: int = 4
    length: int = 2

    @t.override
    def run(self: t.Self) -> None:
        a = self.get_parameter(0)
        self.computer.output(a)

    def __str__(self: t.Self) -> str:
        a = self.raw_parameters[0]
        a_mode = self.parameter_modes[0].name
        return f"{yellow("OUT")} {bright_green(f"{a=}")} {green(f"({a_mode})")}"

class HLT(Instruction):
    name:   str = "HLT"
    opcode: int = 99
    length: int = 1

    @t.override
    def run(self: t.Self) -> None:
        pass

    def __str__(self: t.Self) -> str:
        return yellow("HLT")

class IntcodeComputer:
    debug_log: bool
    debug_log_ip_len: int

    memory: list[int]
    instruction_pointer: int

    inputs:  deque[int]
    outputs: list[int]

    def __init__(self: t.Self, debug_log: bool = False) -> None:
        self.debug_log = debug_log
        self.debug_log_ip_len = 1
        self.init_ip()
        self.inputs = deque()
        self.outputs = []

    def init_ip(self: t.Self, address: int = 0) -> t.Self:
        self.instruction_pointer = address
        return self

    def load_memory(self: t.Self, data: list[int]) -> t.Self:
        self.memory = data.copy()
        self.debug_log_ip_len = len(str(len(self.memory)))
        return self

    def peek_memory(self: t.Self, address: int) -> int | t.NoReturn:
        return next(self.read_memory(address, 1))

    def read_memory(self: t.Self, starting_address: int, length: int) -> t.Iterable[int] | t.NoReturn:
        if length == 0:
            yield
        else:
            if not (0 <= starting_address < len(self.memory)):
                raise IndexError(f"starting address {starting_address} out of memory")
            if not (starting_address + (length - 1) < len(self.memory)):
                raise IndexError(f"reading {length} bytes from starting address {starting_address} reaches out of memory")

            yield from self.memory[starting_address:starting_address + length]

    def queue_inputs(self: t.Self, future_inputs: t.Iterable[int]) -> t.Self:
        self.inputs.extend(future_inputs)
        return self

    def get_input(self: t.Self) -> int:
        return self.inputs.popleft()

    def output(self: t.Self, value: int) -> None:
        self.outputs.append(value)
        if self.debug_log:
            print(f"[{red(f"{"OUT": >{self.debug_log_ip_len}}")}] {blue(value)}")

    def step(self: t.Self) -> bool:
        current_instruction: Instruction = Instruction.get(self, self.instruction_pointer)

        if self.debug_log:
            print(f"[{cyan(f"{self.instruction_pointer: >{self.debug_log_ip_len}}")}] {current_instruction}")

        current_instruction.run()

        if current_instruction.name == "HLT":
            return False
        self.instruction_pointer += current_instruction.length
        return True

    def run(self: t.Self) -> t.Self:
        while self.step():
            pass
        return self
