"""The day four solution to Advent of Code."""

from collections import Counter
from itertools import repeat
from pathlib import Path
from typing import Literal, cast

from aoc_core import Part

type Line = str
type Lines = list[Line]
type Word = str
type LineIndex = int
type CharIndex = int
type Anchor = tuple[LineIndex, CharIndex]
type Orientation = Literal[
    "RIGHT", "LEFT", "UP", "DOWN", "UPRIGHT", "UPLEFT", "DOWNRIGHT", "DOWNLEFT"
]
type Match = tuple[Anchor, Orientation]
type Matches = list[Match]

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")


def load_input(*, test: bool = False) -> Lines:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT

    with input_path.open("r", encoding="utf-8") as file:
        return list(filter(None, map(str.strip, file.readlines())))


def get_matches(lines: Lines, word: Word) -> Matches:  # noqa: C901
    """Find matches for a given word in the lines."""
    n_lines = len(lines)
    line_length = len(lines[0])
    word_length = len(word)

    matches = []
    for line_index, line in enumerate(lines):
        check_down = line_index <= (n_lines - word_length)
        check_up = line_index >= (word_length - 1)

        line_lists = [(list(repeat(line, word_length)), "")]
        if check_down:
            line_lists.append((lines[line_index : line_index + word_length], "DOWN"))
        if check_up:
            end_index: int | None = line_index - word_length
            if end_index == -1:
                end_index = None
            line_lists.append((lines[line_index:end_index:-1], "UP"))

        for char_index, char in enumerate(line):
            if char != word[0]:
                continue

            check_right = char_index <= (line_length - word_length)
            check_left = char_index >= (word_length - 1)

            char_index_lists = [(list(repeat(char_index, word_length)), "")]
            if check_right:
                char_index_lists.append(
                    (list(range(char_index, char_index + word_length)), "RIGHT")
                )
            if check_left:
                char_index_lists.append(
                    (list(range(char_index, char_index - word_length, -1)), "LEFT")
                )

            for line_list_idx, (line_list, line_orient) in enumerate(line_lists):
                for char_l_idx, (char_index_list, char_orient) in enumerate(char_index_lists):
                    if line_list_idx == 0 and char_l_idx == 0:
                        continue
                    chars = [l[idx] for l, idx in zip(line_list, char_index_list, strict=True)]  # noqa: E741
                    if "".join(chars) == word:
                        orientation = cast(Orientation, f"{line_orient}{char_orient}")
                        matches.append(((line_index, char_index), orientation))

    return matches


def part_one(lines: Lines) -> None:
    """Perform part one of the Advent of Code solution."""
    matches = get_matches(lines, "XMAS")
    print(f"Part one: {len(matches)} matches")


def part_two(lines: Lines) -> None:
    """Perform part two of the Advent of Code solution."""
    matches = get_matches(lines, "MAS")
    match_centres = []
    for anchor, orientation in matches:
        if orientation == "UPRIGHT":
            match_centres.append((anchor[0] - 1, anchor[1] + 1))
        elif orientation == "UPLEFT":
            match_centres.append((anchor[0] - 1, anchor[1] - 1))
        elif orientation == "DOWNRIGHT":
            match_centres.append((anchor[0] + 1, anchor[1] + 1))
        elif orientation == "DOWNLEFT":
            match_centres.append((anchor[0] + 1, anchor[1] - 1))

    count = sum(value > 1 for value in Counter(match_centres).values())
    print(f"Part two: {count} matches")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the fourth Advent of Code problem."""
    lines = load_input(test=test)

    if part in ("one", "both"):
        part_one(lines)

    if part in ("two", "both"):
        part_two(lines)
