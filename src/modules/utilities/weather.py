"""Weather lookups for Zen-Bot.

Uses the free, key-less wttr.in JSON API so it works out of the box. The parsing
is separated from the network call so it can be unit-tested with a fixed sample.
"""

from __future__ import annotations

import requests

_URL = "https://wttr.in/{location}?format=j1"


def parse_current(data: dict, location: str) -> str:
    """Turn a wttr.in JSON payload into a one-line spoken summary."""
    try:
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels = current["FeelsLikeC"]
        desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
    except (KeyError, IndexError, TypeError):
        return f"Sorry, I couldn't read the weather for {location}."
    return (
        f"It's {temp_c} degrees in {location}, {desc.lower()}, "
        f"feels like {feels} degrees, humidity {humidity} percent."
    )


def current(location: str, timeout: float = 6.0) -> str:
    """Fetch the current weather for a location."""
    location = location.strip() or "here"
    try:
        resp = requests.get(_URL.format(location=location), timeout=timeout)
        resp.raise_for_status()
        return parse_current(resp.json(), location)
    except requests.RequestException:
        return f"Sorry, I couldn't reach the weather service for {location}."
