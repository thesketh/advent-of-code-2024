"""The day five solution to Advent of Code."""

from pathlib import Path

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")


def load_input(*, test: bool = False) -> None:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT  # noqa: F841
    raise NotImplementedError("Input parser not implemented yet.")


def part_one() -> None:
    """Perform part one of the Advent of Code solution."""
    raise NotImplementedError("Part one not implemented yet.")


def part_two() -> None:
    """Perform part two of the Advent of Code solution."""
    raise NotImplementedError("Part two not implemented yet.")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the fifth Advent of Code problem."""
    lines = load_input(test=test)

    if part in ("one", "both"):
        part_one(lines)

    if part in ("two", "both"):
        part_two(lines)
