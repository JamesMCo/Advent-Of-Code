#!/usr/bin/env python3

#Advent of Code
#Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

ingredients = []
for ingredient in puzzle_input:
    ingredient = ingredient.split()
    ingredients.append([int(x) for x in [ingredient[2][:-1], ingredient[4][:-1], ingredient[6][:-1], ingredient[8][:-1], ingredient[10]]])

def score(amounts):
    running = []
    for i in range(4):
        working = 0
        for j, amount in enumerate(amounts):
            working += amount * ingredients[j][i]
        if working < 0:
            running.append(0)
        else:
            running.append(working)

    working = 1
    for val in running:
        working *= val
    return working

def increment(quant_list):
    i = len(quant_list) - 1
    while i >= 0:
        quant_list[i] += 1
        if quant_list[i] == 101:
            quant_list[i] = 0
            i -= 1
        else:
            break
    return quant_list

highest = 0
quants = [0 for x in range(len(ingredients))]
end_state = [100 for x in range(len(ingredients))]
while True:
    must_run = True
    while sum(quants) != 100 or must_run:
        must_run = False
        quants = increment(quants)
        if quants == end_state:
            print("The total score of the highest-scoring cookie is " + str(highest) + ".")
            exit()
    temp = score(quants)
    if temp > highest:
        highest = temp
