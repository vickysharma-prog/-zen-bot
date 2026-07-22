from src.core.router import CommandRouter
from src.modules.productivity.tasks import TaskStore


def make_router():
    # Network disabled so weather routing is deterministic in tests.
    return CommandRouter(TaskStore(":memory:"), enable_network=False)


def test_greeting_and_identity():
    r = make_router()
    assert "Hello" in r.route("hello there")
    assert "Zen" in r.route("what is your name")


def test_time_and_date():
    r = make_router()
    assert "time is" in r.route("what time is it").lower()
    assert "today is" in r.route("what's the date").lower()


def test_system_routes():
    r = make_router()
    assert "CPU" in r.route("what's my cpu usage")
    assert "Memory" in r.route("how much ram am I using")


def test_calculator_route():
    r = make_router()
    assert r.route("calculate 6 times 7") == "The answer is 42."
    assert r.route("what is 2 + 2") == "The answer is 4."


def test_units_route():
    r = make_router()
    assert "miles" in r.route("convert 10 km to miles")


def test_tasks_route():
    r = make_router()
    assert "Added task" in r.route("add task: buy milk")
    assert "1 pending" in r.route("show my tasks")


def test_weather_route_without_network():
    r = make_router()
    assert "network" in r.route("what's the weather in Delhi").lower()


def test_unknown_falls_through_to_ai():
    r = make_router()
    # Not a built-in skill -> None so the caller uses the AI.
    assert r.route("tell me a story about dragons") is None
