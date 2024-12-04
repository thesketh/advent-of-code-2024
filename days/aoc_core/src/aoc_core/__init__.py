"""Core functionality for Advent of Code."""

from typing import Annotated, Literal, Protocol

from pydantic import Field

Day = Annotated[int, Field(ge=1, lt=25)]
Part = Literal["one", "two", "both"]


class Runner(Protocol):
    """A function to run the Advent of Code solution for a given day."""

    @staticmethod
    def __call__(part: Part, *, test: bool = False) -> None: ...  # noqa: D102
