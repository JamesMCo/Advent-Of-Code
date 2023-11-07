from collections import defaultdict, deque
from enum import IntEnum
from util.colour import *
import typing as t

class ParameterMode(IntEnum):
    POSITION  = 0
    IMMEDIATE = 1
    RELATIVE  = 2

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

    def get_parameter(self: t.Self, num: int, is_output: bool = False) -> int:
        if is_output:
            # Get address, not value from memory, so that the address can be written to
            match self.parameter_modes[num]:
                case ParameterMode.POSITION:  return self.raw_parameters[num]
                case ParameterMode.IMMEDIATE: raise RuntimeError("Parameters that an instruction writes to will never be in immediate mode.")
                case ParameterMode.RELATIVE:  return self.computer.relative_base + self.raw_parameters[num]
        else:
            # Get the value from memory
            match self.parameter_modes[num]:
                case ParameterMode.POSITION:  return self.computer.peek_memory(self.raw_parameters[num])
                case ParameterMode.IMMEDIATE: return self.raw_parameters[num]
                case ParameterMode.RELATIVE:  return self.computer.peek_memory(self.computer.relative_base + self.raw_parameters[num])

    def run(self: t.Self) -> bool:
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
    def run(self: t.Self) -> bool:
        a   = self.get_parameter(0)
        b   = self.get_parameter(1)
        out = self.get_parameter(2, True)
        self.computer.memory[out] = a + b
        return True

    def __str__(self: t.Self) -> str:
        a, b, out = self.raw_parameters
        a_mode, b_mode, out_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("ADD")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")} {bright_magenta(f"{out=}")} {magenta(f"({out_mode})")}"

class MUL(Instruction):
    name:   str = "MUL"
    opcode: int = 2
    length: int = 4

    @t.override
    def run(self: t.Self) -> bool:
        a   = self.get_parameter(0)
        b   = self.get_parameter(1)
        out = self.get_parameter(2, True)
        self.computer.memory[out] = a * b
        return True

    def __str__(self: t.Self) -> str:
        a, b, out = self.raw_parameters
        a_mode, b_mode, out_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("MUL")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")} {bright_magenta(f"{out=}")} {magenta(f"({out_mode})")}"

class INP(Instruction):
    name:   str = "INP"
    opcode: int = 3
    length: int = 2

    @t.override
    def run(self: t.Self) -> bool:
        out = self.get_parameter(0, True)
        input_value = self.computer.get_input()
        if input_value is None:
            # No input able to be read
            return False
        else:
            self.computer.memory[out] = input_value
            return True

    def __str__(self: t.Self) -> str:
        out = self.raw_parameters[0]
        out_mode = self.parameter_modes[0].name
        return f"{yellow("INP")} {bright_magenta(f"{out=}")} {green(f"({out_mode})")}"

class OUT(Instruction):
    name:   str = "OUT"
    opcode: int = 4
    length: int = 2

    @t.override
    def run(self: t.Self) -> bool:
        a = self.get_parameter(0)
        self.computer.output(a)
        return True

    def __str__(self: t.Self) -> str:
        a = self.raw_parameters[0]
        a_mode = self.parameter_modes[0].name
        return f"{yellow("OUT")} {bright_green(f"{a=}")} {green(f"({a_mode})")}"

class JIT(Instruction):
    name:   str = "JIT"
    opcode: int = 5
    length: int = 3

    @t.override
    def run(self: t.Self) -> bool:
        a = self.get_parameter(0)
        b = self.get_parameter(1)
        if a != 0:
            self.computer.init_ip(b)
        return True

    def __str__(self: t.Self) -> str:
        a, b = self.raw_parameters
        a_mode, b_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("JIT")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")}"

class JIF(Instruction):
    name:   str = "JIF"
    opcode: int = 6
    length: int = 3

    @t.override
    def run(self: t.Self) -> bool:
        a = self.get_parameter(0)
        b = self.get_parameter(1)
        if a == 0:
            self.computer.init_ip(b)
        return True

    def __str__(self: t.Self) -> str:
        a, b = self.raw_parameters
        a_mode, b_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("JIF")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")}"

class LSS(Instruction):
    name:   str = "LSS"
    opcode: int = 7
    length: int = 4

    @t.override
    def run(self: t.Self) -> bool:
        a   = self.get_parameter(0)
        b   = self.get_parameter(1)
        out = self.get_parameter(2, True)
        self.computer.memory[out] = int(a < b)
        return True

    def __str__(self: t.Self) -> str:
        a, b, out = self.raw_parameters
        a_mode, b_mode, out_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("LSS")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")} {bright_magenta(f"{out=}")} {magenta(f"({out_mode})")}"

class EQL(Instruction):
    name:   str = "EQL"
    opcode: int = 8
    length: int = 4

    @t.override
    def run(self: t.Self) -> bool:
        a   = self.get_parameter(0)
        b   = self.get_parameter(1)
        out = self.get_parameter(2, True)
        self.computer.memory[out] = int(a == b)
        return True

    def __str__(self: t.Self) -> str:
        a, b, out = self.raw_parameters
        a_mode, b_mode, out_mode = [mode.name for mode in self.parameter_modes]
        return f"{yellow("EQL")} {bright_green(f"{a=}")} {green(f"({a_mode})")} {bright_green(f"{b=}")} {green(f"({b_mode})")} {bright_magenta(f"{out=}")} {magenta(f"({out_mode})")}"

class ARB(Instruction):
    name:   str = "ARB"
    opcode: int = 9
    length: int = 2

    @t.override
    def run(self: t.Self) -> bool:
        a = self.get_parameter(0)
        self.computer.init_rb(self.computer.relative_base + a)
        return True

    def __str__(self: t.Self) -> str:
        a = self.raw_parameters[0]
        a_mode = self.parameter_modes[0].name
        return f"{yellow("ARB")} {bright_green(f"{a=}")} {green(f"({a_mode})")}"

class HLT(Instruction):
    name:   str = "HLT"
    opcode: int = 99
    length: int = 1

    @t.override
    def run(self: t.Self) -> bool:
        self.computer.halted = True
        return True

    def __str__(self: t.Self) -> str:
        return yellow("HLT")

class IntcodeComputer:
    debug_log: bool
    debug_log_ip_len: int

    initial_memory: list[int]
    memory: t.DefaultDict[int, int]
    instruction_pointer: int
    relative_base: int

    inputs:  deque[int]
    outputs: list[int]
    output_listeners: list[t.Callable[[int], t.Any]]

    halted: bool = False

    def __init__(self: t.Self, debug_log: bool = False) -> None:
        self.debug_log = debug_log
        self.debug_log_ip_len = 1
        self.init_ip()
        self.init_rb()
        self.inputs = deque()
        self.outputs = []
        self.output_listeners = []
        self.halted = False

    def init_ip(self: t.Self, address: int = 0) -> t.Self:
        self.instruction_pointer = address
        return self

    def init_rb(self: t.Self, address: int = 0) -> t.Self:
        self.relative_base = address
        return self

    def load_memory(self: t.Self, data: list[int]) -> t.Self:
        self.initial_memory = data.copy()
        self.memory = defaultdict(int)
        for address, value in enumerate(data):
            self.memory[address] = value
        self.debug_log_ip_len = len(str(len(self.memory)))
        return self

    def reset(self: t.Self) -> t.Self:
        self.memory = defaultdict(int)
        for address, value in enumerate(self.initial_memory):
            self.memory[address] = value
        self.init_ip()
        self.init_rb()
        self.inputs.clear()
        self.outputs.clear()
        self.halted = False
        return self

    def peek_memory(self: t.Self, address: int) -> int | t.NoReturn:
        return next(self.read_memory(address, 1))

    def read_memory(self: t.Self, starting_address: int, length: int) -> t.Iterable[int] | t.NoReturn:
        if length == 0:
            yield
        else:
            if starting_address < 0:
                raise IndexError(f"starting address {starting_address} out of memory")
            elif length < 0:
                raise IndexError(f"reading {length} bytes from starting address {starting_address} reaches out of memory")

            yield from (self.memory[address] for address in range(starting_address, starting_address + length))

    def get_memory_as_list(self: t.Self) -> list[int]:
        return [self.memory[address] for address in range(0, max(self.memory.keys()) + 1)]

    def queue_inputs(self: t.Self, future_inputs: int | t.Iterable[int]) -> t.Self:
        if isinstance(future_inputs, int):
            self.inputs.append(future_inputs)
        else:
            self.inputs.extend(future_inputs)
        return self

    def get_input(self: t.Self) -> t.Optional[int]:
        if self.inputs:
            return self.inputs.popleft()
        else:
            return None

    def register_output_listener(self: t.Self, callback: t.Callable[[int], t.Any]):
        self.output_listeners.append(callback)

    def output(self: t.Self, value: int) -> None:
        self.outputs.append(value)

        if self.debug_log:
            print(f"[{red(f"{"OUT": >{self.debug_log_ip_len}}")}] {blue(value)}")

        for listener in self.output_listeners:
            listener(value)

    def step(self: t.Self) -> bool:
        if not self.halted:
            current_instruction: Instruction = Instruction.get(self, self.instruction_pointer)

            if self.debug_log:
                print(f"[{cyan(f"{self.instruction_pointer: >{self.debug_log_ip_len}}")}] {current_instruction}")

            before_instruction_pointer: int = self.instruction_pointer
            if current_instruction.run():
                # Instruction ran successfully
                if before_instruction_pointer == self.instruction_pointer:
                    # Instruction pointer was not modified (i.e. by jumping)
                    self.instruction_pointer += current_instruction.length
            else:
                # Instruction did not run successfully (e.g. INP when no inputs)
                # Do not try to move the instruction pointer
                pass
        return not self.halted

    def run(self: t.Self) -> t.Self:
        while not self.halted:
            self.step()
        return self
