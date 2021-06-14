#!/usr/bin/env python3

import colorama, os

colorama.init(strip=False)

if os.name == "nt":
    s = ""
else:
    s = "python ./"

names = ["",
         "Inverse Captcha", "Corruption Checksum", "Spiral Memory", "High-Entropy Passphrases", "A Maze of Twisty Trampolines, All Alike",
         "Memory Reallocation", "Recursive Circus", "I Heard You Like Registers", "Stream Processing", "Knot Hash",
         "Hex Ed", "Digital Plumber", "Packet Scanners", "Disk Defragmentation", "Dueling Generators",
         "Permutation Promenade", "Spinlock", "Duet", "A Series of Tubes", "Particle Swarm",
         "Fractal Art", "Sporifica Virus", "Coprocessor Conflagration", "Electromagnetic Moat", "The Halting Problem"]

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
