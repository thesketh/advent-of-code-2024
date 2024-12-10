"""The day eight solution to Advent of Code."""

from collections import defaultdict
from functools import partial
from itertools import count, product
from pathlib import Path
from typing import Literal

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")

type Char = str
type Empty = Literal["."]
type GridRow = list[Char | Empty]
type Grid = list[GridRow]
type XIndex = int
type YIndex = int
type GridReference = tuple[XIndex, YIndex]
type AntennaMapping = dict[Char, list[GridReference]]

EMPTY: Literal[Empty] = "."


def load_input(*, test: bool = False) -> Grid:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT
    with input_path.open("r", encoding="utf-8") as input_file:
        return [list(row.strip()) for row in input_file if row.strip()]


def scan_characters(grid: Grid) -> AntennaMapping:
    """Scan the mapping of characters to group by antenna type."""
    characters: dict[Char, list[GridReference]] = defaultdict(list)
    for y_index, row in enumerate(grid):
        for x_index, char in enumerate(row):
            if char != EMPTY:
                characters[char].append((x_index, y_index))
    return characters


def check_grid_reference_bounds(
    grid_reference: GridReference, x_max_exclusive: int, y_max_exclusive: int
) -> bool:
    """Check the bounds of a grid reference."""
    x_in_range = grid_reference[0] in range(x_max_exclusive)
    y_in_range = grid_reference[1] in range(y_max_exclusive)
    return x_in_range and y_in_range


def count_antinodes(grid: Grid, *, include_resonant_harmonics: bool = False) -> int:
    """Count the antinodes in an antenna grid."""
    in_bounds = partial(
        check_grid_reference_bounds, y_max_exclusive=len(grid), x_max_exclusive=len(grid[0])
    )
    antenna_mapping = scan_characters(grid)

    min_distance = 0 if include_resonant_harmonics else 2

    antinodes = set()
    for grid_references in antenna_mapping.values():
        if len(grid_references) == 1:
            continue

        for position_a, position_b in product(grid_references, grid_references):
            if position_a == position_b:
                continue

            x_diff = position_b[0] - position_a[0]
            y_diff = position_b[1] - position_a[1]
            for dist in count(min_distance):
                any_valid = False
                for antinode in (
                    (position_a[0] + (dist * x_diff), position_a[1] + (dist * y_diff)),
                    (position_b[0] - (dist * x_diff), position_b[1] - (dist * y_diff)),
                ):
                    if in_bounds(antinode):
                        antinodes.add(antinode)
                        any_valid = True
                if not any_valid or not include_resonant_harmonics:
                    break
    return len(antinodes)


def part_one(grid: Grid) -> None:
    """Perform part one of the Advent of Code solution."""
    print(f"Part one: {count_antinodes(grid)} antinodes")


def part_two(grid: Grid) -> None:
    """Perform part two of the Advent of Code solution."""
    print(f"Part two: {count_antinodes(grid, include_resonant_harmonics=True)} antinodes")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the eighth Advent of Code problem."""
    grid = load_input(test=test)

    if part in ("one", "both"):
        part_one(grid)

    if part in ("two", "both"):
        part_two(grid)
