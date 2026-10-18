
from tools.tasks import add_task


def test_add_task_rejects_empty_input():
    result = add_task.invoke({"task": "   "})

    assert result == "Error: Task description cannot be empty."


def test_add_task_accepts_valid_input():
    result = add_task.invoke({"task": "Test task"})

    assert result == "Task added successfully"
