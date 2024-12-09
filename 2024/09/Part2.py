#!/usr/bin/env python3

#Advent of Code
#2024 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from typing import Generator, Optional, Self

def solve(puzzle_input: list[int]) -> int:
    class Node:
        prev_node: Optional[Self]
        next_node: Optional[Self]
        file_id: Optional[int]
        length: Optional[int]

        def __init__(self: Self, file_id: Optional[int] = None, length: Optional[int] = None) -> None:
            self.prev_node = None
            self.next_node = None
            self.file_id = file_id
            self.length = length

    class LinkedList:
        head: Optional[Node]
        tail: Optional[Node]

        def __init__(self: Self) -> None:
            self.head = None
            self.tail = None

        def append(self: Self, node: Node) -> None:
            # Append a node to the end of the list
            if self.head is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next_node = node
                node.prev_node = self.tail
                self.tail = node

        def remove(self: Self, node: Node) -> None:
            # Remove a node from the list, preserving links between adjacent nodes
            if node.prev_node is not None:
                node.prev_node.next_node = node.next_node
            if node.next_node is not None:
                node.next_node.prev_node = node.prev_node

            if node == self.head:
                self.head = node.next_node
            if node == self.tail:
                self.tail = node.prev_node

        def insert_into_free(self: Self, target: Node, node: Node) -> None:
            # If the target node is free space, insert the new node at the start of the free space
            if target.file_id is not None: return
            if target.length is None or node.length is None: return
            if target.length < node.length: return

            if target.length == node.length:
                target.file_id = node.file_id
            else:
                if target.prev_node:
                    node.prev_node = target.prev_node
                    target.prev_node.next_node = node
                if target == self.head:
                    self.head = node
                target.prev_node = node
                node.next_node = target
                target.length -= node.length

        def remove_zero_lengths(self: Self) -> None:
            # Remove nodes with a length of 0 from the list
            curr_node: Optional[Node] = self.head
            while curr_node:
                if curr_node.length is None or curr_node.length == 0:
                    empty_node: Node = curr_node
                    curr_node = curr_node.next_node
                    self.remove(empty_node)
                else:
                    curr_node = curr_node.next_node

        def squash(self: Self) -> None:
            # Merge adjacent nodes with the same file id
            curr_node: Optional[Node] = self.head
            while curr_node:
                if curr_node.next_node and curr_node.file_id == curr_node.next_node.file_id:
                    curr_node.length += curr_node.next_node.length
                    self.remove(curr_node.next_node)
                curr_node = curr_node.next_node

        def compact(self: Self) -> None:
            # Implement part 2 file moving logic
            curr_node: Optional[Node] = self.tail
            while curr_node:
                if curr_node.file_id:
                    scan_pointer: Optional[Node] = self.head
                    while scan_pointer and scan_pointer != curr_node:
                        if scan_pointer.file_id is None and scan_pointer.length >= curr_node.length:
                            self.insert_into_free(scan_pointer, Node(curr_node.file_id, curr_node.length))
                            curr_node.file_id = None
                            break
                        scan_pointer = scan_pointer.next_node
                curr_node = curr_node.prev_node

    filesystem: LinkedList = LinkedList()

    is_file: bool = True
    curr_id: int = -1
    for digit in puzzle_input:
        filesystem.append(Node((curr_id := curr_id + 1) if is_file else None, digit))
        is_file = not is_file

    filesystem.remove_zero_lengths()
    filesystem.squash()
    filesystem.compact()

    def get_compacted_blocks() -> Generator[int | None]:
        curr_node: Node = filesystem.head
        while curr_node:
            for _ in range(curr_node.length):
                yield curr_node.file_id
            curr_node = curr_node.next_node

    return sum(position * file_id for position, file_id in enumerate(get_compacted_blocks()) if file_id is not None)

def main() -> tuple[str, int]:
    puzzle_input = [int(n) for n in util.read.as_string()]

    return "The filesystem checksum is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([int(n) for n in "2333133121414131402"]), 2858)

run(main)
