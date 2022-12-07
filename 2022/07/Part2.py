#!/usr/bin/env python3

#Advent of Code
#2022 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class File:
        def __init__(self, name, parent, size):
            self.is_directory = False
            self.name         = name
            self.parent       = parent
            self.size         = int(size)

        def get_size(self):
            return self.size

    class Directory:
        def __init__(self, name, parent=None):
            self.is_directory = True
            self.name         = name
            self.parent       = parent
            self.children     = {}

        def add_child(self, descriptor):
            data, name = descriptor.split()
            if data == "dir":
                self.children[name] = Directory(name, self)
            else:
                self.children[name] = File(name, self, data)

        def get_size(self):
            return sum(child.get_size() for child in self.children.values())

        def get_directories(self):
            directories = [self]
            for child in self.children.values():
                if child.is_directory:
                    directories.extend(child.get_directories())
            return directories

    root = Directory("/")
    cwd  = root
    i = 0
    while i < len(puzzle_input):
        match puzzle_input[i][2:].split():
            case ["cd", "/"]:
                cwd = root
                i += 1
            case ["cd", ".."]:
                cwd = cwd.parent
                i += 1
            case ["cd", relative_dir]:
                cwd = cwd.children[relative_dir]
                i += 1
            case ["ls"]:
                i += 1
                while i < len(puzzle_input) and not puzzle_input[i].startswith("$"):
                    cwd.add_child(puzzle_input[i])
                    i += 1

    free_space = 70000000 - root.get_size()
    target = 30000000 - free_space


    return min([directory.get_size() for directory in root.get_directories() if directory.get_size() >= target])

def main():
    puzzle_input = util.read.as_lines()

    size = solve(puzzle_input)

    print("The size of the smallest directory that, if deleted, would free up enough space to run the system update is " + str(size) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["$ cd /",
                                       "$ ls",
                                       "dir a",
                                       "14848514 b.txt",
                                       "8504156 c.dat",
                                       "dir d",
                                       "$ cd a",
                                       "$ ls",
                                       "dir e",
                                       "29116 f",
                                       "2557 g",
                                       "62596 h.lst",
                                       "$ cd e",
                                       "$ ls",
                                       "584 i",
                                       "$ cd ..",
                                       "$ cd ..",
                                       "$ cd d",
                                       "$ ls",
                                       "4060174 j",
                                       "8033020 d.log",
                                       "5626152 d.ext",
                                       "7214296 k"]), 24933642)

run(main)
