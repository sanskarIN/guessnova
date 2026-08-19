"""Hint generation that stays useful without revealing the answer."""

from __future__ import annotations

from .domain import Difficulty


def smart_hint(target: int, guess: int, difficulty: Difficulty) -> str:
    distance = abs(target - guess)
    ratio = distance / max(1, difficulty.span - 1)
    if ratio <= 0.02:
        temperature = "scorching hot"
    elif ratio <= 0.08:
        temperature = "hot"
    elif ratio <= 0.2:
        temperature = "warm"
    elif ratio <= 0.4:
        temperature = "cool"
    else:
        temperature = "cold"

    parity = "even" if target % 2 == 0 else "odd"
    direction = "higher" if target > guess else "lower"
    return f"{temperature}; try {direction}. The target is {parity}."
