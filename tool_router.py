
def select_tool(message: str) -> str:
    """Select a tool using Persian and English keywords."""

    text = message.lower().strip()

    # 1. List tasks
    if any(word in text for word in [
        "list tasks",
        "show tasks",
        "my tasks",
        "فهرست وظایف",
        "نمایش وظایف",
        "وظایفم",
        "کارهایم",
    ]):
        return "list_tasks"

    # 2. Add a task
    if any(word in text for word in [
        "add task",
        "create task",
        "new task",
        "وظیفه جدید",
        "ثبت وظیفه",
        "اضافه کن",
        "یادآوری کار",
    ]):
        return "add_task"

    # 3. Get notes
    if any(word in text for word in [
        "show notes",
        "get notes",
        "my notes",
        "یادداشت‌هایم",
        "یادداشت ها",
        "نمایش یادداشت",
        "یادداشت‌ها را نشان بده",
    ]):
        return "get_notes"

    # 4. Save a note
    if any(word in text for word in [
        "save note",
        "remember this",
        "take a note",
        "یادداشت کن",
        "ذخیره یادداشت",
        "این را ثبت کن",
        "به خاطر بسپار",
    ]):
        return "save_note"

    # 5. Calculator
    if any(word in text for word in [
        "calculate",
        "calculator",
        "what is",
        "حاصل",
        "محاسبه",
        "حساب کن",
        "چند می‌شود",
        "چقدر می‌شود",
    ]):
        return "calculator"

    return "unknown"
