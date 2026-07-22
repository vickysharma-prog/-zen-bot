from src.modules.productivity.tasks import TaskStore, handle


def make_store():
    return TaskStore(":memory:")


def test_add_and_list():
    s = make_store()
    s.add("buy groceries")
    s.add("call mom", priority="high")
    tasks = s.list()
    assert len(tasks) == 2
    assert tasks[0].text == "buy groceries"
    assert tasks[1].priority == "high"


def test_complete_hides_from_default_list():
    s = make_store()
    t = s.add("write report")
    assert s.complete(t.id) is True
    assert s.list() == []
    assert len(s.list(include_done=True)) == 1


def test_complete_missing():
    s = make_store()
    assert s.complete(999) is False


def test_handle_add_and_priority():
    s = make_store()
    msg = handle("add task: submit assignment", s)
    assert "Added task" in msg
    msg2 = handle("add task: urgent fix the bug", s)
    assert s.list()[-1].priority == "high"


def test_handle_list_and_complete():
    s = make_store()
    handle("add task: one", s)
    assert "1 pending" in handle("list my tasks", s)
    assert "done" in handle("complete task 1", s).lower()


def test_handle_non_task_returns_none():
    assert handle("what's the weather", make_store()) is None
