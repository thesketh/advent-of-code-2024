"""The day six solution to Advent of Code."""

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal, cast

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")

type Direction = Literal["up", "down", "left", "right"]
type Distance = int
type GuardMarker = Literal["^", ">", "v", "<"]
type Obstacle = Literal["#"]
type FreeSpace = Literal["."]
type GridMarker = Obstacle | FreeSpace
type GridRow = list[GridMarker]
type Grid = list[GridRow]
type Visited = set[Guard]

OBSTACLE: Obstacle = "#"
FREE_SPACE: FreeSpace = "."
GUARD_MARKER_MAPPING: dict[GuardMarker, Direction] = {
    "^": "up",
    ">": "right",
    "v": "down",
    "<": "left",
}


class InLoopError(Exception):
    """An error raised when a loop is encountered."""


class OutOfBoundsError(Exception):
    """An error raised when a guard goes out of bounds."""


@dataclass(frozen=True)
class Position:
    """A position within a grid."""

    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        """Move the point in a given direction, returning a new position."""
        cls = type(self)
        x, y = self.x, self.y

        if direction == "up":
            new = cls(x=x, y=y - 1)
        elif direction == "down":
            new = cls(x=x, y=y + 1)
        elif direction == "right":
            new = cls(x=x + 1, y=y)
        elif direction == "left":
            new = cls(x=x - 1, y=y)
        return new

    def in_bounds(self, upper_x_bound: int, upper_y_bound: int) -> bool:
        """Check whether the point is in bounds."""
        return (0 <= self.y <= upper_y_bound) and (0 <= self.x <= upper_x_bound)


@dataclass(frozen=True)
class Guard:
    """A guard with a position and direction."""

    TURN_MAPPING: ClassVar[dict[Direction, Direction]] = {
        "up": "right",
        "right": "down",
        "down": "left",
        "left": "up",
    }
    """A mapping of directions the guard should turn to when hitting an obstacle."""

    position: Position
    direction: Direction

    def move(self) -> "Guard":
        """Move the guard."""
        return type(self)(position=self.position.move(self.direction), direction=self.direction)

    def turn(self) -> "Guard":
        """Turn the guard."""
        return type(self)(position=self.position, direction=self.TURN_MAPPING[self.direction])

    def in_bounds(self, upper_x_bound: int, upper_y_bound: int) -> bool:
        """Check whether the guard is in bounds."""
        return self.position.in_bounds(upper_x_bound, upper_y_bound)

    def patrol(self, grid: Grid, visited: Visited | None = None) -> Iterator["Guard"]:
        """Patrol a grid, yielding the guard at each step."""
        visited = visited.copy() if visited else set()
        upper_y_bound = len(grid) - 1
        upper_x_bound = len(grid[0]) - 1

        guard = self
        yield guard

        while True:
            if guard in visited:
                raise InLoopError("The guard's route will loop and never finish")
            visited.add(guard)

            new_guard = guard.move()
            if not new_guard.in_bounds(upper_x_bound, upper_y_bound):  # Patrol finished.
                return

            if grid[new_guard.position.y][new_guard.position.x] == FREE_SPACE:
                guard = new_guard
                yield guard
            else:  # No point in yielding the guard if all they've done is turn
                guard = guard.turn()

    def patrol_will_loop(self, grid: Grid, visited: Visited | None = None) -> bool:
        """Check whether a guard's patrol will loop."""
        try:
            all(self.patrol(grid, visited))
        except InLoopError:
            return True
        return False


def load_input(*, test: bool = False) -> tuple[Grid, Guard]:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT

    grid: Grid = []
    lines = [line.strip() for line in input_path.read_text().split("\n") if line.strip()]
    guard: Guard | None = None

    for line_index, line in enumerate(lines):
        row: GridRow = []
        for char_index, char in enumerate(line):
            if char in (FREE_SPACE, OBSTACLE):
                row.append(cast(GridMarker, char))
                continue

            if char not in GUARD_MARKER_MAPPING:
                raise ValueError(f"Unexpected character in input: {char}")
            if guard is not None:
                raise ValueError("Only one guard expected")

            position = Position(x=char_index, y=line_index)
            guard = Guard(
                position=position, direction=GUARD_MARKER_MAPPING[cast(GuardMarker, char)]
            )
            row.append(FREE_SPACE)

        grid.append(row)

    if guard is None:
        raise ValueError("No guard found")
    return grid, guard


def part_one(grid: Grid, guard: Guard) -> None:
    """Perform part one of the Advent of Code solution."""
    unique_positions = len({guard.position for guard in guard.patrol(grid)})
    print(f"Part one: {unique_positions} unique positions")


def build_new_grid(grid: Grid, obstacle_position: Position) -> Grid:
    """Build a new grid without a full deep copy."""
    x, y = obstacle_position.x, obstacle_position.y
    new_grid = grid.copy()
    new_row = grid[y].copy()
    new_row[x] = OBSTACLE
    new_grid[y] = new_row
    return new_grid


def part_two(grid: Grid, guard: Guard) -> None:
    """Perform part two of the Advent of Code solution."""
    route = guard.patrol(grid)
    guard = next(route)

    visited: Visited = set()
    tried_obstacles = set()

    n_looped_patrols = 0
    for next_guard in route:
        if (obstacle_position := next_guard.position) not in tried_obstacles:
            new_grid = build_new_grid(grid, obstacle_position)
            n_looped_patrols += guard.patrol_will_loop(new_grid, visited)
            tried_obstacles.add(obstacle_position)
        visited.add(guard)
        guard = next_guard

    print(f"Part one: {n_looped_patrols} possible patrol loops")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the sixth Advent of Code problem."""
    grid, guard = load_input(test=test)

    if part in ("one", "both"):
        part_one(grid, guard)

    if part in ("two", "both"):
        part_two(grid, guard)
