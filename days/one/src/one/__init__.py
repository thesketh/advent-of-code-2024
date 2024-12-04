"""The day one solution to Advent of Code."""

import re
from collections import Counter
from pathlib import Path

from aoc_core import Part

type LocationList = list[int]
type LeftList = LocationList
type RightList = LocationList

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")


def load_input(*, test: bool = False) -> tuple[LeftList, RightList]:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT

    with input_path.open("r", encoding="utf-8") as file:
        lines = filter(None, map(str.strip, file))
        entries = [map(int, re.split(r"\s+", line, maxsplit=1)) for line in lines]
        left_entries, right_entries = map(list, zip(*entries, strict=True))
        return left_entries, right_entries


def part_one(left_list: LeftList, right_list: RightList) -> None:
    """Perform part one of the Advent of Code solution."""
    left_list = sorted(left_list)
    right_list = sorted(right_list)
    distance = sum(abs(left - right) for (left, right) in zip(left_list, right_list, strict=True))
    print(f"Part one: {distance} total distance between locations")


def part_two(left_list: LeftList, right_list: RightList) -> None:
    """Perform part two of the Advent of Code solution."""
    value_scores = Counter(right_list)
    for value in value_scores:
        value_scores[value] *= value
    similarity_score = sum(value_scores[value] for value in left_list)
    print(f"Part two: {similarity_score} total similarity score")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the first Advent of Code problem."""
    left_list, right_list = load_input(test=test)

    if part in ("one", "both"):
        part_one(left_list, right_list)

    if part in ("two", "both"):
        part_two(left_list, right_list)
