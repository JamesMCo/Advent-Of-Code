#!/usr/bin/env python3

import colorama, os, time, yaml

colorama.init()

if os.name == "nt":
    s = ""
else:
    s = "python ./"

if time.gmtime().tm_mon == 12:
    year = time.gmtime().tm_year
else:
    year = time.gmtime().tm_year - 1

with open(f"docs/_data/{year}.yml") as f:
    names = [day["name"] for day in sorted([full_day for full_day in yaml.safe_load(f)], key=lambda x: x["day"])]

os.chdir(str(year))

printed = False
p_day   = False
for day in range(1, 26):
    if os.path.isdir(str(day).zfill(2)):
        os.chdir(str(day).zfill(2))
        if os.path.isfile("Part1.py"):
            if printed:
                print("\n")
            sep = "*" * len(f"**  Day {day}  - {names[day - 1]}  **")
            print(f"{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}**  Day {day}  - {names[day - 1]}  **{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n\n\n{colorama.Fore.GREEN}Testing Part 1{colorama.Fore.RESET}\n")
            p_day = True
            
            r = os.system(s + "Part1.py")
            if r:
                exit(r)

            printed = True
        if os.path.isfile("Part2.py"):
            if printed:
                print("\n")
            if not p_day:
                sep = "*" * len(f"**  Day {day}  - {names[day - 1]}  **")
                print(f"{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}**  Day {day}  - {names[day - 1]}  **{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n\n\n{colorama.Fore.GREEN}Testing Part 2{colorama.Fore.RESET}\n")
            else:
                print(f"{colorama.Fore.GREEN}Testing Part 2{colorama.Fore.RESET}\n")
            
            r = os.system(s + "Part2.py")
            if r:
                exit(r)

            printed = True
        os.chdir("..")
