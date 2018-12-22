#!/usr/bin/env python3

import colorama, os

colorama.init()

if os.name == "nt":
    s = ""
else:
    s = "python ./"

names = ["",
         "Chronal Calibration", "Inventory Management System", "No Matter How You Slice It", "Repose Record", "Alchemical Reduction",
         "Chronal Coordinates", "The Sum of Its Parts", "Memory Maneuver", "Marble Mania", "The Stars Align",
         "Chronal Charge", "Subterranean Sustainability", "Mine Cart Madness", "Chocolate Charts", "Beverage Bandits",
         "Chronal Classification", "Reservoir Research", "Settlers of The North Pole", "Go With The Flow", "A Regular Map",
         "Chronal Conversion", "Mode Maze", "", "", ""]

printed = False
p_day   = False
for day in range(1, 26):
    if os.path.isdir(str(day).zfill(2)):
        os.chdir(str(day).zfill(2))
        if os.path.isfile("Part1.py"):
            if printed:
                print("\n")
            sep = "*" * len(f"**  Day {day}  - {names[day]}  **")
            print(f"{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}**  Day {day}  - {names[day]}  **{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n\n\n{colorama.Fore.GREEN}Testing Part 1{colorama.Fore.RESET}\n")
            p_day = True
            
            r = os.system(s + "Part1.py")
            if r:
                exit(r)

            printed = True
        if os.path.isfile("Part2.py"):
            if printed:
                print("\n")
            if not p_day:
                sep = "*" * len(f"**  Day {day}  - {names[day]}  **")
                print(f"{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}**  Day {day}  - {names[day]}  **{colorama.Fore.RESET}\n{colorama.Fore.YELLOW}{sep}{colorama.Fore.RESET}\n\n\n{colorama.Fore.GREEN}Testing Part 2{colorama.Fore.RESET}\n")
            else:
                print(f"{colorama.Fore.GREEN}Testing Part 2{colorama.Fore.RESET}\n")
            
            r = os.system(s + "Part2.py")
            if r:
                exit(r)

            printed = True
        os.chdir("..")
