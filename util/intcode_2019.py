from dataclasses import dataclass
from util.colour import *
import typing as t

@dataclass
class InstructionData:
    name:   str
    opcode: int
    length: int

    @staticmethod
    def run(computer: "IntcodeComputer", parameters: list[int]):
        raise NotImplementedError()

    @staticmethod
    def str(parameters: list[int]) -> str:
        raise NotImplementedError()

class ADD(InstructionData):
    def __init__(self: t.Self) -> None:
        super().__init__("ADD", 1, 4)

    @staticmethod
    @t.override
    def run(computer: "IntcodeComputer", parameters: list[int]) -> None:
        a, b, out = parameters
        computer.memory[out] = computer.peek_memory(a) + computer.peek_memory(b)

    @staticmethod
    def str(parameters: list[int]) -> str:
        a, b, out = parameters
        return f"{yellow("ADD")} {green(f"{a=}")} {green(f"{b=}")} {magenta(f"{out=}")}"

class MUL(InstructionData):
    def __init__(self: t.Self) -> None:
        super().__init__("MUL", 2, 4)

    @staticmethod
    @t.override
    def run(computer: "IntcodeComputer", parameters: list[int]) -> None:
        a, b, out = parameters
        computer.memory[out] = computer.peek_memory(a) * computer.peek_memory(b)

    @staticmethod
    def str(parameters: list[int]) -> str:
        a, b, out = parameters
        return f"{yellow("MUL")} {green(f"{a=}")} {green(f"{b=}")} {magenta(f"{out=}")}"

class HLT(InstructionData):
    def __init__(self: t.Self) -> None:
        super().__init__("HLT", 99, 1)

    @staticmethod
    @t.override
    def run(computer: "IntcodeComputer", parameters: list[int]) -> None:
        pass

    @staticmethod
    def str(parameters: list[int]) -> str:
        return yellow("HLT")

class Instruction:
    ADD: InstructionData = ADD()
    MUL: InstructionData = MUL()
    HLT: InstructionData = HLT()

    _instructions: t.Optional[dict[int, InstructionData]] = None
    @classmethod
    def get(cls: t.Self, opcode: int) -> InstructionData | t.NoReturn:
        if cls._instructions is None:
            cls._instructions = {attr.opcode: attr for attr in cls.__dict__.values() if isinstance(attr, InstructionData)}

        return cls._instructions[opcode]

class IntcodeComputer:
    debug_log: bool
    debug_log_ip_len: int

    memory: list[int]
    instruction_pointer: int

    def __init__(self: t.Self, debug_log: bool = False) -> None:
        self.debug_log = debug_log
        self.debug_log_ip_len = 1
        self.init_ip()

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

    def step(self: t.Self) -> bool:
        current_instruction: InstructionData = Instruction.get(self.peek_memory(self.instruction_pointer))
        parameters: list[int] = list(self.read_memory(self.instruction_pointer + 1, current_instruction.length - 1))

        if self.debug_log:
            print(f"[{cyan(f"{self.instruction_pointer: >{self.debug_log_ip_len}}")}] {current_instruction.str(parameters)}")

        current_instruction.run(self, parameters)

        if current_instruction == Instruction.HLT:
            return False
        self.instruction_pointer += current_instruction.length
        return True

    def run(self: t.Self) -> t.Self:
        while self.step():
            pass
        return self
