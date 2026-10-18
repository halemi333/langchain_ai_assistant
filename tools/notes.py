import json
import os

from langchain_core.tools import tool

NOTES_FILE = "data/notes.json"

@tool
def save_note(content: str) -> str:
    """
    Save a note provided by the user.

    Args:
        content:
            The text content of the note.

    Returns:
        Confirmation message.
    """

    try:

        if os.path.exists(NOTES_FILE):

            with open(
                NOTES_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                notes = json.load(f)

        else:

            notes = []

        notes.append(content)

        with open(
            NOTES_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                notes,
                f,
                ensure_ascii=False,
                indent=4
            )

        return "Note saved successfully"

    except Exception as e:

        return f"Error: {str(e)}"

@tool
def get_notes() -> str:
    """
    Get all saved notes.

    Returns:
        List of saved notes.
    """

    try:

        if not os.path.exists(NOTES_FILE):

            return "No notes found"

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            notes = json.load(f)

        return "\n".join(notes)

    except Exception as e:

        return f"Error: {str(e)}"