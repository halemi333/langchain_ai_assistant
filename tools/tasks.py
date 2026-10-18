import json
import os

from langchain_core.tools import tool

TASKS_FILE = "data/tasks.json"

@tool
def add_task(task: str) -> str:
    """
    Create a new task.

    Args:
        task:
            The task description.

    Returns:
        Confirmation message.
    """

    try:

        task = task.strip()

        if not task:
            return "Error: Task description cannot be empty."

        if os.path.exists(TASKS_FILE):

            with open(
                TASKS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                tasks = json.load(f)

        else:

            tasks = []

        tasks.append(
            {
                "task": task,
                "completed": False
            }
        )

        with open(
            TASKS_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                tasks,
                f,
                ensure_ascii=False,
                indent=4
            )

        return "Task added successfully"

    except Exception as e:

        return f"Error: {str(e)}"

@tool
def list_tasks() -> str:
    """
    List all created tasks.

    Returns:
        All tasks with their status.
    """

    try:

        if not os.path.exists(TASKS_FILE):

            return "No tasks found"

        with open(
            TASKS_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            tasks = json.load(f)

        if not tasks:

            return "No tasks found"

        result = []

        for index, item in enumerate(tasks, start=1):

            status = (
                "Done"
                if item["completed"]
                else "Pending"
            )

            result.append(
                f"{index}. {item['task']} - {status}"
            )

        return "\n".join(result)

    except Exception as e:

        return f"Error: {str(e)}"