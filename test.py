#!/usr/bin/env python3

import argparse, colorama, os, time, yaml

if time.gmtime().tm_mon == 12:
    current_year = time.gmtime().tm_year
else:
    current_year = time.gmtime().tm_year - 1

parser = argparse.ArgumentParser(description="Runs either the current year's or a given year's tests", allow_abbrev=False)
parser.add_argument("year", help="specify which year to test", nargs="?", default=current_year)
args = parser.parse_args()

colorama.init()

if os.name == "nt":
    s = ""
else:
    s = "python ./"

with open(f"docs/_data/{args.year}.yml") as f:
    names = [day["name"] for day in sorted([full_day for full_day in yaml.safe_load(f)], key=lambda x: x["day"] if isinstance(x["day"], int) else 26)]

open("times.txt", "w").close()

os.chdir(str(args.year))

printed = False
for day in range(1, 26):
    p_day = False
    if os.path.isdir(str(day).zfill(2)):
        os.chdir(str(day).zfill(2))
        for part in [1, 2]:
            if os.path.isfile(f"Part{part}.py"):
                if printed:
                    print("\n")
                if not p_day:
                    sep = "*" * len(f"**  Day {day}  - {names[day - 1]}  **")
                    print(f"{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}**  Day {day}  - {names[day - 1]}  **{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n\n\n{colorama.Fore.GREEN}Testing Part {part}{colorama.Fore.RESET}\n")
                else:
                    print(f"{colorama.Fore.GREEN}Testing Part {part}{colorama.Fore.RESET}\n")

                r = os.system(s + f"Part{part}.py")
                if r:
                    exit(r)

                printed = True
                p_day = True
        os.chdir("..")
os.chdir("..")

with open("times.txt") as f:
    duration = str(round(sum(float(t) for t in f), 3))
    duration += "0" * (3 - len(duration.split(".")[1]))

    print(f"\n{colorama.Fore.CYAN}All solutions found in {colorama.Fore.GREEN}{duration}s{colorama.Fore.CYAN}.{colorama.Fore.RESET}")

os.remove("times.txt")