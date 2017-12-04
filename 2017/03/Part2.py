#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = int(f.read()[:-1])
f.close()

x = y = 0

grid = {(0, 0): 1}
max_coord = 0
first_stage_0 = False
last_calculated = 1

def get_grid(x, y):
    try:
        to_return = grid[(x,y)]
        return to_return
    except:
        grid[(x,y)] = 0
        return grid[(x,y)]

stage = 3 #0 is moving up, 1 left, 2 down and 3 right
while last_calculated < puzzle_input:
    print((x,y), last_calculated)
    if stage == 0:
        if first_stage_0:
            max_coord += 1
            y += 1
            first_stage_0 = False
        if y == -max_coord:
            stage = 1
        else:
            y -= 1
    elif stage == 1:
        if x == -max_coord:
            stage = 2
        else:
            x -= 1
    elif stage == 2:
        if y == max_coord:
            stage = 3
        else:
            y += 1
    elif stage == 3:
        if x == max_coord:
            stage = 0
            first_stage_0 = True
        x += 1

    grid[(x,y)] = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            else:
                grid[(x,y)] += get_grid(x+i,y+j)
    last_calculated = grid[(x,y)]

print("The first value written that is greater than the puzzle input is " + str(grid[(x,y)]) + ".")
