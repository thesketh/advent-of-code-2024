"""The day two solution to Advent of Code."""

from collections.abc import Iterable, Iterator
from itertools import tee
from pathlib import Path

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")

type Level = int
type Report = list[Level]
type Reports = list[Report]


MIN_SAFE_THRESHOLD: Level = 1
MAX_SAFE_THRESHOLD: Level = 3
SAFE_RANGE = range(MIN_SAFE_THRESHOLD, MAX_SAFE_THRESHOLD + 1)


def pairwise[T](iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
    """
    Iterate over an iterable pairwise, returning the value and the
    next value in a tuple.

    """
    current_iter, next_iter = tee(iter(iterable))
    try:
        next(next_iter)
    except StopIteration:
        return iter([])
    return zip(current_iter, next_iter, strict=False)


def load_input(*, test: bool = False) -> Reports:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT

    with input_path.open("r", encoding="utf-8") as file:
        lines = filter(None, map(str.strip, file))
        return [list(map(int, line.split())) for line in lines]


def check_report_safe(report: Report) -> bool:
    """Return whether a report is safe."""
    n_transitions = len(report) - 1
    diffs = (next_ - current for current, next_ in pairwise(report))
    sign_safe = ((-1 if diff < 0 else 1, abs(diff) in SAFE_RANGE) for diff in diffs)
    n_safe_transitions = abs(sum(sign if safe else 0 for sign, safe in sign_safe))
    return n_safe_transitions == n_transitions


def check_report_safe_with_skips(report: Report) -> bool:
    """Return whether a report is safe, allowing a single skipped value."""
    if check_report_safe(report):
        return True

    for skip_index in range(len(report)):
        new_report = report[:skip_index] + report[skip_index + 1 :]
        if check_report_safe(new_report):
            return True
    return False


def part_one(reports: Reports) -> None:
    """Perform part one of the Advent of Code solution."""
    safe_count = sum(map(check_report_safe, reports))
    print(f"Part one: {safe_count} reports are safe")


def part_two(reports: Reports) -> None:
    """Perform part two of the Advent of Code solution."""
    safe_count = sum(map(check_report_safe_with_skips, reports))
    print(f"Part two: {safe_count} reports are safe")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the second Advent of Code problem."""
    reports = load_input(test=test)

    if part in ("one", "both"):
        part_one(reports)

    if part in ("two", "both"):
        part_two(reports)
