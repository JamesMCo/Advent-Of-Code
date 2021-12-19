#!/usr/bin/env python3

#Advent of Code
#2021 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import ceil, floor

def solve(puzzle_input):
    class Leaf:
        def __init__(self, data, parent=None):
            self.parent = parent
            self.value = data

        def root(self):
            n = self
            while n.parent is not None:
                n = n.parent
            return n

        def list_repr(self):
            return [self]

        def replace(self, o):
            if self.parent.left == self:
                self.parent.left = o
            elif self.parent.right == self:
                self.parent.right = o
            o.parent = self.parent

        def can_explode(self):
            return False

        def can_split(self):
            return self.value >= 10

        def split(self):
            self.replace(Tree([floor(self.value / 2), ceil(self.value / 2)]))

        def magnitude(self):
            return self.value

        def pprint(self, depth=0):
            print(self.value, end="")

    class Tree:
        def __init__(self, data, parent=None):
            self.parent = parent

            if isinstance(data[0], list):
                self.left = Tree(data[0], self)
            elif isinstance(data[0], Tree):
                self.left = data[0]
                self.left.parent = self
            else:
                self.left = Leaf(data[0], self)

            if isinstance(data[1], list):
                self.right = Tree(data[1], self)
            elif isinstance(data[1], Tree):
                self.right = data[1]
                self.right.parent = self
            else:
                self.right = Leaf(data[1], self)

        def root(self):
            n = self
            while n.parent is not None:
                n = n.parent
            return n

        def list_repr(self):
            return self.left.list_repr() + self.right.list_repr()

        def replace(self, o):
            if self.parent.left == self:
                self.parent.left = o
            elif self.parent.right == self:
                self.parent.right = o
            o.parent = self.parent

        def can_explode(self):
            root = self.root()
            chain = [self]
            while (chain[-1] != root):
                chain.append(chain[-1].parent)
            return len(chain) >= 5 # Chain includes self, so 4 parents => len(5)

        def explode(self):
            leaves = self.root().list_repr()
            i = leaves.index(self.left)
            if i != 0:
                leaves[i-1].value += self.left.value
            if i != len(leaves) - 2:
                leaves[i+2].value += self.right.value
            self.replace(Leaf(0))

        def can_split(self):
            return False

        def magnitude(self):
            return (3 * self.left.magnitude()) + (2 * self.right.magnitude())

        def pprint(self, depth=0):
            print("[", end="")
            self.left.pprint(depth+1)
            print(",", end="")
            self.right.pprint(depth+1)
            print("]", end="")
            if depth == 0:
                print()

    def reduce_until_stable(number):
        changed = True
        while changed:
            changed = False
            
            # Check for explosions
            for leaf in number.list_repr():
                if leaf.parent.can_explode():
                    leaf.parent.explode()
                    changed = True
                    break
            if changed:
                continue

            # Check for splits
            for leaf in number.list_repr():
                if leaf.can_split():
                    leaf.split()
                    changed = True
                    break
        return number

    puzzle_input = [reduce_until_stable(Tree(eval(line))) for line in puzzle_input]

    final_sum = None
    for line in puzzle_input:
        if final_sum is None:
            final_sum = line
        else:
            final_sum = reduce_until_stable(Tree([final_sum, line]))

    return final_sum.magnitude()

def main():
    puzzle_input = util.read.as_lines()

    magnitude = solve(puzzle_input)

    print("The magnitude of the final sum is " + str(magnitude) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["[9,1]"]), 29)

    def test_ex2(self):
        return self.assertEqual(solve(["[1,9]"]), 21)

    def test_ex3(self):
        return self.assertEqual(solve(["[9,1]",
                                       "[1,9]"]), 129)

    def test_ex4(self):
        return self.assertEqual(solve(["[1,2]",
                                       "[[3,4],5]"]), 143)

    def test_ex5(self):
        return self.assertEqual(solve(["[[[[4,3],4],4],[7,[[8,4],9]]]",
                                       "[1,1]"]), 1384)

    def test_ex6(self):
        return self.assertEqual(solve(["[1,1]",
                                       "[2,2]",
                                       "[3,3]",
                                       "[4,4]"]), 445)

    def test_ex7(self):
        return self.assertEqual(solve(["[1,1]",
                                       "[2,2]",
                                       "[3,3]",
                                       "[4,4]",
                                       "[5,5]"]), 791)

    def test_ex8(self):
        return self.assertEqual(solve(["[1,1]",
                                       "[2,2]",
                                       "[3,3]",
                                       "[4,4]",
                                       "[5,5]",
                                       "[6,6]"]), 1137)

    def test_ex9(self):
        return self.assertEqual(solve(["[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
                                       "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
                                       "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
                                       "[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
                                       "[7,[5,[[3,8],[1,4]]]]",
                                       "[[2,[2,2]],[8,[8,1]]]",
                                       "[2,9]",
                                       "[1,[[[9,3],9],[[9,0],[0,7]]]]",
                                       "[[[5,[7,4]],7],1]",
                                       "[[[[4,2],2],6],[8,7]]"]), 3488)

    def test_ex10(self):
        return self.assertEqual(solve(["[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]",
                                       "[[[5,[2,8]],4],[5,[[9,9],0]]]",
                                       "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]",
                                       "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
                                       "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]",
                                       "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
                                       "[[[[5,4],[7,7]],8],[[8,3],8]]",
                                       "[[9,3],[[9,9],[6,[4,9]]]]",
                                       "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
                                       "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"]), 4140)

run(main)
