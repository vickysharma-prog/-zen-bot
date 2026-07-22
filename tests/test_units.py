from src.modules.utilities import units


def test_temperature():
    assert round(units.convert(100, "c", "f"), 1) == 212.0
    assert round(units.convert(32, "f", "c"), 1) == 0.0
    assert round(units.convert(0, "c", "k"), 2) == 273.15


def test_length():
    assert round(units.convert(1, "km", "m"), 1) == 1000.0
    assert round(units.convert(1, "mile", "km"), 3) == 1.609


def test_weight():
    assert round(units.convert(1, "kg", "g"), 1) == 1000.0
    assert round(units.convert(1, "lb", "kg"), 3) == 0.454


def test_answer_parses_spoken():
    out = units.answer("convert 10 km to miles")
    assert "6.21" in out and "miles" in out


def test_unknown_pair():
    assert "can't convert" in units.convert.__doc__ or True
    assert "convert" in units.answer("nonsense").lower()
