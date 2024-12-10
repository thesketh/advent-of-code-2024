"""The day seven solution to Advent of Code."""

import math
from collections.abc import Sequence
from operator import add, mul
from pathlib import Path
from typing import Protocol, cast

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")

type TestValue = int
type CalibrationNumbers = Sequence[int]
type Calibration = tuple[TestValue, CalibrationNumbers]
type Calibrations = list[Calibration]


class Operator(Protocol):
    """An operator which acts on two numbers."""

    @staticmethod
    def __call__(v1: int, v2: int, /) -> int: ...  # noqa: D102


def load_input(*, test: bool = False) -> Calibrations:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT
    with input_path.open("r", encoding="utf-8") as input_file:
        split_lines = (line.strip().split(": ") for line in input_file)
        return [(int(test_value), list(map(int, eqn.split()))) for test_value, eqn in split_lines]


def evaluate_total_calibration_result(
    calibrations: Calibrations, operators: Sequence[Operator]
) -> int:
    """Evaluate the total calibration result, given some operators."""
    running_total = 0
    for test_value, calibration_numbers in calibrations:
        accumulators = list(calibration_numbers[:1])
        for number in calibration_numbers[1:]:
            new_accumulators: list[int] = []
            for current_value in accumulators:
                new_accumulators.extend(operator(current_value, number) for operator in operators)
            accumulators = new_accumulators
        if test_value in set(accumulators):
            running_total += test_value
    return running_total


def concat(v1: int, v2: int) -> int:
    """Concatenate two integers as strings."""
    return cast(int, (v1 * (10 ** (int(math.log10(v2)) + 1))) + v2)


def part_one(calibrations: Calibrations) -> None:
    """Perform part one of the Advent of Code solution."""
    running_total = evaluate_total_calibration_result(calibrations, (add, mul))
    print(f"Part one: {running_total} total calibration result")


def part_two(calibrations: Calibrations) -> None:
    """Perform part two of the Advent of Code solution."""
    running_total = evaluate_total_calibration_result(calibrations, (add, mul, concat))
    print(f"Part two: {running_total} total calibration result")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the seventh Advent of Code problem."""
    calibrations = load_input(test=test)

    if part in ("one", "both"):
        part_one(calibrations)

    if part in ("two", "both"):
        part_two(calibrations)
