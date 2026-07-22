"""Unit conversions for Zen-Bot.

Handles temperature, length and weight conversions from spoken requests such as
"convert 10 km to miles" or "20 celsius to fahrenheit".
"""

from __future__ import annotations

import re

# Length units expressed in metres.
_LENGTH = {
    "m": 1.0, "meter": 1.0, "meters": 1.0, "metre": 1.0, "metres": 1.0,
    "km": 1000.0, "kilometer": 1000.0, "kilometers": 1000.0,
    "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01,
    "mm": 0.001,
    "mi": 1609.344, "mile": 1609.344, "miles": 1609.344,
    "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
    "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
    "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
}

# Weight units expressed in grams.
_WEIGHT = {
    "g": 1.0, "gram": 1.0, "grams": 1.0,
    "kg": 1000.0, "kilogram": 1000.0, "kilograms": 1000.0,
    "mg": 0.001,
    "lb": 453.592, "lbs": 453.592, "pound": 453.592, "pounds": 453.592,
    "oz": 28.3495, "ounce": 28.3495, "ounces": 28.3495,
}

_TEMP = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}


class ConversionError(ValueError):
    pass


def _convert_temp(value: float, src: str, dst: str) -> float:
    src, dst = src[0], dst[0]  # c/f/k
    # to celsius
    if src == "c":
        c = value
    elif src == "f":
        c = (value - 32) * 5 / 9
    else:  # kelvin
        c = value - 273.15
    # from celsius
    if dst == "c":
        return c
    if dst == "f":
        return c * 9 / 5 + 32
    return c + 273.15


def _convert_scale(value: float, src: str, dst: str, table: dict) -> float:
    return value * table[src] / table[dst]


def convert(value: float, src: str, dst: str) -> float:
    """Convert value from unit src to unit dst."""
    src, dst = src.lower(), dst.lower()
    if src in _TEMP and dst in _TEMP:
        return _convert_temp(value, src, dst)
    if src in _LENGTH and dst in _LENGTH:
        return _convert_scale(value, src, dst, _LENGTH)
    if src in _WEIGHT and dst in _WEIGHT:
        return _convert_scale(value, src, dst, _WEIGHT)
    raise ConversionError(f"can't convert {src} to {dst}")


_PATTERN = re.compile(
    r"(-?\d+(?:\.\d+)?)\s*([a-z]+)\s+(?:to|in|into)\s+([a-z]+)", re.IGNORECASE
)


def answer(text: str) -> str:
    """Speech-friendly answer for a conversion request."""
    m = _PATTERN.search(text)
    if not m:
        return "Tell me what to convert, for example: convert 10 km to miles."
    value, src, dst = float(m.group(1)), m.group(2), m.group(3)
    try:
        result = convert(value, src, dst)
    except ConversionError as exc:
        return f"Sorry, {exc}."
    return f"{value:g} {src} is {result:.2f} {dst}."
