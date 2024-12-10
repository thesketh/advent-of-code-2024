"""The CLI for the Advent of Code runner."""

import sys  # noqa: I001
from argparse import ArgumentParser, Namespace

# fmt: off
import one
import two
import three
import four
import five
import six
import seven
import eight
import nine
# fmt: on
from aoc_core import Day, Part, Runner
from pydantic import TypeAdapter


class _RunnerArgs(Namespace):
    """The arguments from the parser."""

    day: Day
    part: Part
    test: bool


_RUNNERS: dict[Day, Runner] = {
    1: one.run,
    2: two.run,
    3: three.run,
    4: four.run,
    5: five.run,
    6: six.run,
    7: seven.run,
    8: eight.run,
    9: nine.run,
}
"""Runners for Advent of Code days."""


def _parse_args(argv: list[str]) -> _RunnerArgs:
    """Build a parser and parse command line arguments."""
    parser = ArgumentParser()
    parser.add_argument(
        "day",
        type=TypeAdapter(Day).validate_python,
        help="The day to run the AoC submission for",
    )
    parser.add_argument(
        "-p",
        "--part",
        type=TypeAdapter(Part).validate_python,
        help="The part of the challenge to run",
        default="both",
    )
    parser.add_argument("-t", "--test", help="Use the test data", action="store_true")
    return parser.parse_args(argv, _RunnerArgs())


def main(argv: list[str]) -> None:
    """Run an Advent of Code entry using provided CLI args."""
    args = _parse_args(argv)
    try:
        runner = _RUNNERS[args.day]
    except KeyError as err:
        raise NotImplementedError(f"{args.day} is not implemented yet") from err

    runner(args.part, test=args.test)


def run() -> None:
    """Run an Advent of Code entry using the program's argv."""
    return main(sys.argv[1:])


if __name__ == "__main__":
    run()
