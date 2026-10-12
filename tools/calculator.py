from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Args:
        expression:
            A mathematical expression like 2+2 or 5*10.

    Returns:
        The calculated result.
    """

    try:

        result = eval(expression)

        return str(result)

    except Exception as e:

        return f"Error: {str(e)}"