from src.modules.utilities import weather

# A trimmed wttr.in j1 payload, so parsing is tested without a network call.
SAMPLE = {
    "current_condition": [
        {
            "temp_C": "28",
            "FeelsLikeC": "30",
            "humidity": "65",
            "weatherDesc": [{"value": "Partly cloudy"}],
        }
    ]
}


def test_parse_current():
    out = weather.parse_current(SAMPLE, "Delhi")
    assert "28 degrees in Delhi" in out
    assert "partly cloudy" in out
    assert "65 percent" in out


def test_parse_bad_payload():
    assert "couldn't read" in weather.parse_current({}, "Nowhere")
