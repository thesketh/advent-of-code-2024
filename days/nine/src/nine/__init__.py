"""The day nine solution to Advent of Code."""

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from itertools import count
from pathlib import Path

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")


@dataclass
class FileSystemNode:
    """A node on the filesystem."""

    id: int | None
    occupied: int
    free: int

    def __post_init__(self) -> None:
        if self.id is None and self.occupied:
            raise ValueError("`id` must be non-null if `occupied` is nonzero")


type FileSystem = deque[FileSystemNode]


def load_input(*, test: bool = False) -> FileSystem:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT
    numbers = list(map(int, input_path.read_text().rstrip()))

    filesystem: FileSystem = deque()
    for first_index in range(0, len(numbers), 2):
        occupied = numbers[first_index]
        try:
            free = numbers[first_index + 1]
        except IndexError:
            free = 0

        filesystem.append(FileSystemNode(id=first_index // 2, occupied=occupied, free=free))
    return filesystem


def calculate_checksum(filesystem: FileSystem) -> int:
    """Calculate the checksum for a filesystem."""
    checksum = 0
    counter = count()
    for entry in filesystem:
        if entry.id is None:
            continue
        for _ in range(entry.occupied):
            checksum += next(counter) * entry.id
        for _ in range(entry.free):
            next(counter)
    return checksum


def compact(filesystem: FileSystem) -> FileSystem:
    """Build a densely packed filesystem from the input."""
    filesystem = deepcopy(filesystem)
    new_filesystem: FileSystem = deque()

    free_space = 0
    while filesystem:
        node = filesystem.popleft()
        new_filesystem.append(node)

        while node.free:
            try:
                end_node = filesystem.pop()
            except IndexError:
                free_space += node.free
                node.free = 0
                break

            new_node_id = end_node.id
            if node.free >= end_node.occupied:
                new_node_occupied = end_node.occupied
                node.free -= new_node_occupied
                free_space += end_node.free
            else:
                new_node_occupied = node.free
                node.free = 0
                end_node.occupied -= new_node_occupied
                filesystem.append(end_node)

            free_space += new_node_occupied
            new_filesystem.append(
                FileSystemNode(id=new_node_id, occupied=new_node_occupied, free=0)
            )
    new_filesystem.append(FileSystemNode(id=None, occupied=0, free=free_space))
    return new_filesystem


def compact_whole_files(filesystem: FileSystem) -> FileSystem:
    """Build a densely packed filesystem from the input transferring only whole files."""
    filesystem = deepcopy(filesystem)
    moved = set()

    for file in list(reversed(filesystem))[:-2]:
        if file.id in moved:
            continue

        for move_index, potential_move in enumerate(filesystem):
            if potential_move is file:
                break

            if file.occupied > potential_move.free:
                continue

            new_free = potential_move.free - file.occupied
            new_node = FileSystemNode(id=file.id, occupied=file.occupied, free=new_free)
            filesystem.insert(move_index + 1, new_node)

            file.free += file.occupied
            file.occupied = 0
            potential_move.free = 0
            moved.add(file.id)
            break
    return filesystem


def render(filesystem: FileSystem) -> None:
    """Render a filesystem."""
    for node in filesystem:
        print("".join([str(node.id)] * node.occupied), end="")
        print("".join(["."] * node.free), end="")
    print()


def part_one(filesystem: FileSystem) -> None:
    """Perform part one of the Advent of Code solution."""
    checksum = calculate_checksum(compact(filesystem))
    print(f"Part one: checksum is {checksum}")


def part_two(filesystem: FileSystem) -> None:
    """Perform part two of the Advent of Code solution."""
    checksum = calculate_checksum(compact_whole_files(filesystem))
    print(f"Part two: checksum is {checksum}")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the ninth Advent of Code problem."""
    filesystem = load_input(test=test)

    if part in ("one", "both"):
        part_one(filesystem)

    if part in ("two", "both"):
        part_two(filesystem)
