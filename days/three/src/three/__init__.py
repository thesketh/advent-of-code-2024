"""The day three solution to Advent of Code."""

import re
from itertools import starmap
from operator import mul
from pathlib import Path
from typing import Literal

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
PART_ONE_TEST_INPUT = DATA_ROOT.joinpath("test_part_one.txt")
PART_TWO_TEST_INPUT = DATA_ROOT.joinpath("test_part_two.txt")


type Instructions = str


def load_input(part: Literal["one", "two"], *, test: bool = False) -> Instructions:
    """Load the input."""
    test_path = PART_ONE_TEST_INPUT if part == "one" else PART_TWO_TEST_INPUT
    input_path = test_path if test else LIVE_INPUT
    return input_path.read_text()


def eval_matches(instructions: Instructions) -> int:
    """Evaluate the sum of the applied instructions."""
    pattern = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    numbers = (map(int, match.groups()) for match in pattern.finditer(instructions))
    return sum(starmap(mul, numbers))


def part_one(instructions: Instructions) -> None:
    """Perform part one of the Advent of Code solution."""
    total = eval_matches(instructions)
    print(f"Part one: {total} sum of multiplications")


def part_two(instructions: Instructions) -> None:
    """Perform part two of the Advent of Code solution."""
    pattern = re.compile(r"(don't\(\)(.+?))(do(n't)?\(\)|$)", re.DOTALL)
    while match := pattern.search(instructions):
        start, end = match.span(1)
        instructions = instructions[:start] + instructions[end:]

    total = eval_matches(instructions)
    print(f"Part two: {total} sum of multiplications")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the third Advent of Code problem."""
    if part in ("one", "both"):
        instructions = load_input("one", test=test)
        part_one(instructions)

    if part in ("two", "both"):
        instructions = load_input("two", test=test)
        part_two(instructions)
