import os

if os.name == "nt":
    s = ""
else:
    s = "./"

for day in range(1, 25):
    if os.path.isdir(str(day).zfill(2)):
        os.chdir(str(day).zfill(2))
        if os.path.isfile("Part1.py"):
            print(f"*** Testing Day {day} Part 1 ***")
            r = os.system(s + "Part1.py")
            if r:
                exit(r)
        if os.path.isfile("Part2.py"):
            print(f"*** Testing Day {day} Part 2 ***")
            r = os.system(s + "Part2.py")
            if r:
                exit(r)
        os.chdir("../")
