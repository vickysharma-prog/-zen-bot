from src.modules.utilities import calculator


def test_symbolic():
    assert calculator.evaluate("2 + 2") == 4
    assert calculator.evaluate("12 * 5 + 3") == 63
    assert calculator.evaluate("(1 + 2) * 3") == 9


def test_spoken_words():
    assert calculator.evaluate("12 times 5 plus 3") == 63
    assert calculator.evaluate("10 divided by 4") == 2.5
    assert calculator.evaluate("3 to the power of 3") == 27


def test_answer_formats_integers():
    assert calculator.answer("2 + 2") == "The answer is 4."
    assert calculator.answer("10 / 4") == "The answer is 2.5."


def test_rejects_non_math():
    # No injection: names/calls are not valid in the arithmetic grammar.
    assert "couldn't" in calculator.answer("__import__('os')").lower()


def test_empty():
    assert "couldn't" in calculator.answer("calculate").lower()
