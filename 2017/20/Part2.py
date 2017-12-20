#!/usr/bin/env python3

#Advent of Code
#Day 20, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import collections, unittest

def solve(puzzle_input):
    Position     = collections.namedtuple("Position",     ["x", "y", "z"])
    Velocity     = collections.namedtuple("Velocity",     ["x", "y", "z"])
    Acceleration = collections.namedtuple("Acceleration", ["x", "y", "z"])

    particles = []

    positions = {}
    nochange = 0

    class Particle:
        def __init__(self, position, velocity, acceleration):            
            self.position     = Position(*position)
            self.velocity     = Velocity(*velocity)
            self.acceleration = Acceleration(*acceleration)

            particles.append(self)

        def step(self):
            self.velocity = Velocity(self.velocity.x + self.acceleration.x,
                                     self.velocity.y + self.acceleration.y,
                                     self.velocity.z + self.acceleration.z)
            self.position = Position(self.position.x + self.velocity.x,
                                     self.position.y + self.velocity.y,
                                     self.position.z + self.velocity.z)
            if p.position in positions:
                positions[p.position] += 1
            else:
                positions[p.position]  = 1

    furthest = 0
    for p in puzzle_input:
        pos = [int(x) for x in p.split("<")[1].split(">")[0].split(",")]
        vel = [int(x) for x in p.split("<")[2].split(">")[0].split(",")]
        acc = [int(x) for x in p.split("<")[3].split(">")[0].split(",")]
        Particle(pos, vel, acc)

        if max(abs(x) for x in pos) > furthest:
            furthest = max(abs(x) for x in pos)

    max_wait = (furthest**2 + furthest**2 + furthest**2)**0.5
    while nochange <= max_wait:
        count = len(particles)
        positions = {}

        for p in particles:
            p.step()

        new_particles = []
        for p in particles:
            if positions[p.position] == 1:
                new_particles.append(p)
        particles = new_particles

        if len(particles) == count:
            nochange += 1
        else:
            nochange  = 0

    return count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    count = solve(puzzle_input)

    print("The number of particles that remain after all collisions is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>",
                                "p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>",
                                "p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>",
                                "p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>"]), 1)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
