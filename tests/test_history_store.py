from src.core.history_store import HistoryStore


def test_add_and_recent_order():
    h = HistoryStore(":memory:")
    h.add("hi", "hello")
    h.add("what time", "3 pm")
    h.add("thanks", "you're welcome")
    recent = h.recent(limit=2)
    # recent returns the last two turns in chronological order
    assert [r["user"] for r in recent] == ["what time", "thanks"]
    assert recent[-1]["assistant"] == "you're welcome"


def test_clear():
    h = HistoryStore(":memory:")
    h.add("a", "b")
    h.clear()
    assert h.recent() == []
