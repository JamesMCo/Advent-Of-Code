#!/usr/bin/env python3

#Advent of Code
#2016 Day 13, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = int(f.read()[:-1])
f.close()

from math import inf

cx = 1
cy = 1

def getNeighbours(x, y):
    neigbours = set()
    if x != 0:
        a = x-1
        b = y
        if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
            neigbours.add((a, b))
    if y != 0:
        a = x
        b = y-1
        if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
            neigbours.add((a, b))
    a = x+1
    b = y
    if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
        neigbours.add((a, b))
    a = x
    b = y+1
    if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
        neigbours.add((a, b))

    return neigbours

class Vertex:
    def __init__(self, x, y, dist=inf):
        self.x = x
        self.y = y
        self.dist = dist
        self.prev = None

    def __eq__(self, coords):
        return self.x == coords[0] and self.y == coords[1]

    def __hash__(self):
        return hash((self.x, self.y))

def Disjkstra(Graph, source, dest):
    Q = {}
    All = {}

    for v in Graph:
        if v == source:
            Q[(v[0], v[1])] = All[(v[0], v[1])] = Vertex(v[0], v[1], 0)
        else:
            Q[(v[0], v[1])] = All[(v[0], v[1])] = Vertex(v[0], v[1])

    while Q != {}:
        u = min(Q, key=lambda x: Q[x].dist)
        Q.pop(u)
        if u == dest:
            break

        for v in getNeighbours(u[0], u[1]):
            if v in Q:
                alt = All[u].dist + 1
                if alt < Q[v].dist:
                    Q[v].dist = alt
                    Q[v].prev = u

    return All[dest].dist

graph = set()

for y in range(50):
    for x in range(50):
        if (x, y) == (31, 39):
            print("X", end="")
            graph.add((x, y))
            continue
        if bin(x*x + 3*x + 2*x*y + y + y*y + puzzle_input).count("1") % 2 == 1:
            print("#", end="")
        else:
            print(".", end="")
            graph.add((x, y))
    print()


print("The fewest number of steps required to reach (31, 39) is " + str(Disjkstra(graph, (1, 1), (31, 39))) + ".")