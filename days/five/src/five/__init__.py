"""The day five solution to Advent of Code."""

from collections import defaultdict, deque
from collections.abc import Mapping
from pathlib import Path

from aoc_core import Part

ROOT = Path(__file__).resolve().parent
DATA_ROOT = ROOT.joinpath("data")
LIVE_INPUT = DATA_ROOT.joinpath("live.txt")
TEST_INPUT = DATA_ROOT.joinpath("test.txt")

type PageNumber = int
type PriorityRules = Mapping[PageNumber, set[PageNumber]]
type Update = deque[PageNumber]
type Updates = list[Update]


def load_input(*, test: bool = False) -> tuple[PriorityRules, Updates]:
    """Load the input."""
    input_path = TEST_INPUT if test else LIVE_INPUT
    text = input_path.read_text().rstrip("\n")
    rule_block, update_block = text.split("\n\n", 1)

    rule_tuples = [tuple(map(int, rule.split("|"))) for rule in rule_block.split("\n")]
    priority_rules = defaultdict(set)
    for prior_page, page in rule_tuples:
        priority_rules[page].add(prior_page)

    reports = [deque(map(int, string.split(","))) for string in update_block.split("\n")]
    return priority_rules, reports


def get_priority_rules_subset(priority_rules: PriorityRules, update: Update) -> PriorityRules:
    """Get the priority rules subset for a given update."""
    update_numbers = set(update)
    return {page: priority_rules[page] & update_numbers for page in update}


def is_ordered(update: Update, priority_rules_subset: PriorityRules) -> bool:
    """Check whether an update is ordered."""
    missing = set()
    for page_number in reversed(update):
        missing.discard(page_number)
        missing |= priority_rules_subset[page_number]
    return not missing


def get_midpoint_index(length: int) -> int:
    """Get the index of the midpoint of a sequence, given its length."""
    return length // 2 if length % 2 else ((length // 2) - 1)


def part_one(ordered_updates: Updates) -> None:
    """Perform part one of the Advent of Code solution."""
    update_sum = sum(update[get_midpoint_index(len(update))] for update in ordered_updates)
    print(f"Part one: {update_sum} sum of middle page numbers in correct updates")


def part_two(unordered_updates: Updates, unordered_priority_rules: list[PriorityRules]) -> None:
    """Perform part two of the Advent of Code solution."""
    update_sum = 0
    for rule_subset, update in zip(unordered_priority_rules, unordered_updates, strict=True):
        midpoint_index = get_midpoint_index(len(update))

        added: set[PageNumber] = set()
        while len(added) <= midpoint_index:  # No point in sorting right side.
            page_number = update.popleft()
            if rule_subset[page_number] - added:
                update.append(page_number)
            else:
                added.add(page_number)

        update_sum += page_number

    print(f"Part two: {update_sum} sum of middle page numbers in fixed incorrect updates")


def run(part: Part, *, test: bool = False) -> None:
    """Run the solution to the fifth Advent of Code problem."""
    priority_rules, updates = load_input(test=test)

    ordered_updates = []
    unordered_updates = []
    unordered_priority_rules = []
    for update in updates:
        priority_rule_subset = get_priority_rules_subset(priority_rules, update)
        if is_ordered(update, priority_rule_subset):
            ordered_updates.append(update)
        else:
            unordered_updates.append(update)
            unordered_priority_rules.append(priority_rule_subset)

    if part in ("one", "both"):
        part_one(ordered_updates)

    if part in ("two", "both"):
        part_two(unordered_updates, unordered_priority_rules)
