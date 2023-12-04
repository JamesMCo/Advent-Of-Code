def as_string() -> str:
    with open("puzzle_input.txt") as f:
        return f.read().strip()

def as_lines() -> list[str]:
    with open("puzzle_input.txt") as f:
        return f.read().strip().split("\n")

def as_lines_sans_ending_line() -> list[str]:
    with open("puzzle_input.txt") as f:
        return f.read()[:-1].split("\n")

def as_lines_only_rstrip() -> list[str]:
    with open("puzzle_input.txt") as f:
        return f.read().rstrip().split("\n")

def as_string_list(delim) -> list[str]:
    with open("puzzle_input.txt") as f:
        return f.read().strip().split(delim)

def as_int() -> int:
    with open("puzzle_input.txt") as f:
        return int(f.read().strip())

def as_int_list(delim) -> list[int]:
    with open("puzzle_input.txt") as f:
        return [int(x) for x in f.read().strip().split(delim)]
