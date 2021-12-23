#!/usr/bin/env python3

#Advent of Code
#2021 Day 22, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    def overlapping(a, b):
        # Using method described at https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection#aabb_vs._aabb
        return a[0] <= b[1] and a[1] >= b[0] and\
               a[2] <= b[3] and a[3] >= b[2] and\
               a[4] <= b[5] and a[5] >= b[4]

    def fully_contains(r1, r2):
        for x in r2[0:2]:
            for y in r2[2:4]:
                for z in r2[4:6]:
                    if not ((r1[0] <= x <= r1[1]) and (r1[2] <= y <= r1[3]) and (r1[4] <= z <= r1[5])):
                        return False
        return True

    def adjust_regions(regions, new_region, state):
        new_region_list = []
        # For every region
        #  if it overlaps with the new region, split the region into multiple regions
        #  such that they make the shape of the original region minus the overlap
        # If the new region is turning on, add that to the list of regions
        # Return this set of new regions
        for r in regions:
            if not overlapping(r, new_region):
                # No overlap, so no partitions
                new_region_list.append(r)
                continue
            if fully_contains(new_region, r):
                # New region contains r, so no partitions
                continue

            partitions = []
            # We can split the region r into 6 new regions:
            # - below the new region - above the new region
            # - left of the new region - right of the new region
            # - front (expanding to left and right) of new region
            # - back (expanding to left and right) of new region
            # Some of these regions may not exist, depending on the
            # location of the new region relative to the region r
            # For the regions level with the new region, it looks like:
            #       b
            # ----+----+---- (assuming left = -x, right = +x, back = +z, front = -z)
            #  l  |    | r
            #     |    |
            # ----+----+----
            #       f

            # Below
            if new_region[2] > r[2]: # Is there at least one row of cubes below the new region?
                partitions.append((r[0], r[1], r[2], new_region[2] - 1, r[4], r[5]))
            # Above
            if new_region[3] < r[3]: # Is there at least one row of cubes above the new region?
                partitions.append((r[0], r[1], new_region[3] + 1, r[3], r[4], r[5]))
            # Left
            if new_region[0] > r[0]: # Is there at least one column of cubes left of the new region?
                partitions.append((r[0], new_region[0] - 1, max(r[2], new_region[2]), min(r[3], new_region[3]), max(r[4], new_region[4]), min(r[5], new_region[5])))
            # Right
            if new_region[1] < r[1]: # Is there at least one column of cubes right of the new region?
                partitions.append((new_region[1] + 1, r[1], max(r[2], new_region[2]), min(r[3], new_region[3]), max(r[4], new_region[4]), min(r[5], new_region[5])))
            # Front
            if new_region[4] > r[4]: # Is there at least one column of cubes in front of the new region?
                partitions.append((r[0], r[1], max(r[2], new_region[2]), min(r[3], new_region[3]), r[4], new_region[4] - 1))
            # Back
            if new_region[5] < r[5]: # Is there at least one column of cubes behind the new region?
                partitions.append((r[0], r[1], max(r[2], new_region[2]), min(r[3], new_region[3]), new_region[5] + 1, r[5]))

            for p in partitions:
                new_region_list.append((min(p[0], p[1]), max(p[0], p[1]), min(p[2], p[3]), max(p[2], p[3]), min(p[4], p[5]), max(p[4], p[5])))
        if state == "on":
            new_region_list.append(new_region)
        return new_region_list

    regions = []
    for step in puzzle_input:
        state, x1, x2, y1, y2, z1, z2 = re.match("(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", step).groups()

        x1, x2 = min(int(x1), int(x2)), max(int(x1), int(x2))
        y1, y2 = min(int(y1), int(y2)), max(int(y1), int(y2))
        z1, z2 = min(int(z1), int(z2)), max(int(z1), int(z2))

        regions = adjust_regions(regions, (x1, x2, y1, y2, z1, z2), state)

    volume = lambda x1, x2, y1, y2, z1, z2: (x2-x1+1) * (y2-y1+1) * (z2-z1+1)
    return sum([volume(*r) for r in regions])

def main():
    puzzle_input = util.read.as_lines()

    cubes = solve(puzzle_input)

    print("The number of cubes in the region that are on is " + str(cubes) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["on x=-5..47,y=-31..22,z=-19..33",
                                       "on x=-44..5,y=-27..21,z=-14..35",
                                       "on x=-49..-1,y=-11..42,z=-10..38",
                                       "on x=-20..34,y=-40..6,z=-44..1",
                                       "off x=26..39,y=40..50,z=-2..11",
                                       "on x=-41..5,y=-41..6,z=-36..8",
                                       "off x=-43..-33,y=-45..-28,z=7..25",
                                       "on x=-33..15,y=-32..19,z=-34..11",
                                       "off x=35..47,y=-46..-34,z=-11..5",
                                       "on x=-14..36,y=-6..44,z=-16..29",
                                       "on x=-57795..-6158,y=29564..72030,z=20435..90618",
                                       "on x=36731..105352,y=-21140..28532,z=16094..90401",
                                       "on x=30999..107136,y=-53464..15513,z=8553..71215",
                                       "on x=13528..83982,y=-99403..-27377,z=-24141..23996",
                                       "on x=-72682..-12347,y=18159..111354,z=7391..80950",
                                       "on x=-1060..80757,y=-65301..-20884,z=-103788..-16709",
                                       "on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856",
                                       "on x=-52752..22273,y=-49450..9096,z=54442..119054",
                                       "on x=-29982..40483,y=-108474..-28371,z=-24328..38471",
                                       "on x=-4958..62750,y=40422..118853,z=-7672..65583",
                                       "on x=55694..108686,y=-43367..46958,z=-26781..48729",
                                       "on x=-98497..-18186,y=-63569..3412,z=1232..88485",
                                       "on x=-726..56291,y=-62629..13224,z=18033..85226",
                                       "on x=-110886..-34664,y=-81338..-8658,z=8914..63723",
                                       "on x=-55829..24974,y=-16897..54165,z=-121762..-28058",
                                       "on x=-65152..-11147,y=22489..91432,z=-58782..1780",
                                       "on x=-120100..-32970,y=-46592..27473,z=-11695..61039",
                                       "on x=-18631..37533,y=-124565..-50804,z=-35667..28308",
                                       "on x=-57817..18248,y=49321..117703,z=5745..55881",
                                       "on x=14781..98692,y=-1341..70827,z=15753..70151",
                                       "on x=-34419..55919,y=-19626..40991,z=39015..114138",
                                       "on x=-60785..11593,y=-56135..2999,z=-95368..-26915",
                                       "on x=-32178..58085,y=17647..101866,z=-91405..-8878",
                                       "on x=-53655..12091,y=50097..105568,z=-75335..-4862",
                                       "on x=-111166..-40997,y=-71714..2688,z=5609..50954",
                                       "on x=-16602..70118,y=-98693..-44401,z=5197..76897",
                                       "on x=16383..101554,y=4615..83635,z=-44907..18747",
                                       "off x=-95822..-15171,y=-19987..48940,z=10804..104439",
                                       "on x=-89813..-14614,y=16069..88491,z=-3297..45228",
                                       "on x=41075..99376,y=-20427..49978,z=-52012..13762",
                                       "on x=-21330..50085,y=-17944..62733,z=-112280..-30197",
                                       "on x=-16478..35915,y=36008..118594,z=-7885..47086",
                                       "off x=-98156..-27851,y=-49952..43171,z=-99005..-8456",
                                       "off x=2032..69770,y=-71013..4824,z=7471..94418",
                                       "on x=43670..120875,y=-42068..12382,z=-24787..38892",
                                       "off x=37514..111226,y=-45862..25743,z=-16714..54663",
                                       "off x=25699..97951,y=-30668..59918,z=-15349..69697",
                                       "off x=-44271..17935,y=-9516..60759,z=49131..112598",
                                       "on x=-61695..-5813,y=40978..94975,z=8655..80240",
                                       "off x=-101086..-9439,y=-7088..67543,z=33935..83858",
                                       "off x=18020..114017,y=-48931..32606,z=21474..89843",
                                       "off x=-77139..10506,y=-89994..-18797,z=-80..59318",
                                       "off x=8476..79288,y=-75520..11602,z=-96624..-24783",
                                       "on x=-47488..-1262,y=24338..100707,z=16292..72967",
                                       "off x=-84341..13987,y=2429..92914,z=-90671..-1318",
                                       "off x=-37810..49457,y=-71013..-7894,z=-105357..-13188",
                                       "off x=-27365..46395,y=31009..98017,z=15428..76570",
                                       "off x=-70369..-16548,y=22648..78696,z=-1892..86821",
                                       "on x=-53470..21291,y=-120233..-33476,z=-44150..38147",
                                       "off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"]), 2758514936282235)

run(main)
