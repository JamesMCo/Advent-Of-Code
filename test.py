#!/usr/bin/env python3

import argparse, collections, itertools, os, requests, time, types, typing as t, yaml
from decimal import Decimal
from util.colour import *

if time.gmtime().tm_mon == 12:
    current_year = time.gmtime().tm_year
else:
    current_year = time.gmtime().tm_year - 1

parser = argparse.ArgumentParser(description="Runs either the current year's or a given year's tests", allow_abbrev=False)
parser.add_argument("year", help="specify which year to test", nargs="?", default=current_year)
args = parser.parse_args()

class Day:
    day: int
    day_str: str

    dir_exists:   t.Optional[bool]
    input_exists: t.Optional[bool]
    p1_exists:    t.Optional[bool]
    p2_exists:    t.Optional[bool]

    def __init__(self: t.Self, day: int) -> None:
        self.day = day
        self.day_str = f"{self.day:0>2}"

        self.dir_exists   = None
        self.input_exists = None
        self.p1_exists    = None
        self.p2_exists    = None

    def __enter__(self: t.Self) -> t.Self:
        if os.path.isdir(self.day_str):
            os.chdir(self.day_str)
            self.dir_exists = True

            self.p1_exists = os.path.isfile(f"Part1.py")
            self.p2_exists = os.path.isfile(f"Part2.py")

            self.download_input_if_missing()
        else:
            self.dir_exists = False
        return self

    def __exit__(self: t.Self, exc_type: t.Optional[t.Type[BaseException]], exc_val: t.Optional[BaseException], exc_tb: t.Optional[types.TracebackType]) -> bool | t.NoReturn:
        if self.dir_exists:
            os.chdir("..")
        return False

    def download_input_if_missing(self: t.Self) -> None:
        if os.path.isfile("puzzle_input.txt"):
            self.input_exists = True
        else:
            if "jamdroid_input_cache_key" in os.environ:
                r = requests.get(f"https://jamdro.id/api/adventofcode/input/{args.year}/{self.day_str}", headers={"Authorization": f"Bearer {os.environ["jamdroid_input_cache_key"]}"})
                if r.status_code == 200:
                    with open("puzzle_input.txt", "w") as puzzle_input:
                        # Ensure only one newline at end of file
                        # Can't use strip, in case some whitespace at end of final line
                        file_lines = r.text.split("\n")
                        file_lines = list(itertools.dropwhile(lambda l: l == "", file_lines[::-1]))[::-1]
                        puzzle_input.write("\n".join(file_lines) + "\n")

                        self.input_exists = True
                        return
            self.input_exists = False

    def print_header(self: t.Self) -> None:
        sep = "*" * len(f"**  Day {self.day}  - {names[self.day - 1]}  **")
        print(f"{yellow(f"{sep}\n**  Day {self.day}  - {names[self.day - 1]}  **\n{sep}")}\n\n")

    def can_run_any_part(self: t.Self) -> bool:
        return self.can_run_part(1) or self.can_run_part(2)

    def can_run_part(self: t.Self, part_num: int) -> bool:
        match part_num:
            case 1: return self.dir_exists and self.input_exists and self.p1_exists
            case 2: return self.dir_exists and self.input_exists and self.p2_exists

    @staticmethod
    def run_part(part_num: int) -> t.Optional[bool]:
        print(green(f"Testing Part {part_num}\n"))
        return os.system(f"{"" if os.name == "nt" else "python ./"}Part{part_num}.py") != 0

with open(f"docs/_data/{args.year}.yml") as f:
    names = [day["name"] for day in sorted([full_day for full_day in yaml.safe_load(f)], key=lambda x: x["day"] if isinstance(x["day"], int) else 26)]

open("times.txt", "w").close()

os.chdir(str(args.year))

failed = False
for d in range(1, 26):
    with Day(d) as day:
        if day.can_run_any_part():
            day.print_header()

            for part in (1, 2):
                if day.can_run_part(part):
                    with open("../../times.txt", "a") as f:
                        f.write(f"{day.day}-{part}-")
                    if day.run_part(part):
                        failed = True
                        with open("../../times.txt", "a") as f:
                            f.write("fail\n")
                    print("\n")

os.chdir("..")

with open("times.txt") as f:
    total_duration = 0
    durations = collections.defaultdict(lambda: ("Not attempted", "Not attempted"))

    for line in f.read().strip().split("\n"):
        day, part, dur = line.split("-")
        if dur == "fail":
            dur = "Fail"
        elif dur == "skippedonci":
            dur = "Skipped on CI"
        else:
            total_duration += int(dur)
            dur = Decimal(int(dur) / 1_000_000_000).quantize(Decimal("0.001"))
        if part == "1":
            durations[day] = (dur, durations[day][1])
        elif part == "2":
            durations[day] = (durations[day][0], dur)
    if "25" in durations:
        durations["25"] = (durations["25"][0], "N/A")

    total_duration = Decimal(total_duration / 1_000_000_000).quantize(Decimal("0.001"))

    if github_summary := os.getenv("GITHUB_STEP_SUMMARY"):
        with open(github_summary, "w") as g:
            g.write(f"# {current_year} Solution Runtimes\nAll{" non-failed" if failed else ""} solutions found in {total_duration}s.\n| Day | Part 1 | Part 2|\n|-----|--------|-------|\n")
            for day, parts in sorted(durations.items(), key=lambda x: int(x[0])):
                g.write(f"| [{day}{" 🎂" if day == "9" else ""}](https://mrjamesco.uk/Advent-Of-Code/?{current_year}-{day:0>2}) | {parts[0]}{"s" if parts[0] not in ["Not attempted", "Fail", "N/A", "Skipped on CI"] else ""} | {parts[1]}{"s" if parts[1] not in ["Not attempted", "Fail", "N/A", "Skipped on CI"] else ""} |\n")

    print(f"{cyan(f"All{" non-failed" if failed else ""} solutions found in")} {green(f"{total_duration}s")}{cyan(".")}")

os.remove("times.txt")