"""Core functionality for Advent of Code."""

from collections.abc import Iterable, Iterator
from itertools import tee
from typing import Annotated, Literal, Protocol

from pydantic import Field

Day = Annotated[int, Field(ge=1, lt=25)]
Part = Literal["one", "two", "both"]


class Runner(Protocol):
    """A function to run the Advent of Code solution for a given day."""

    @staticmethod
    def __call__(part: Part, *, test: bool = False) -> None: ...  # noqa: D102


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
