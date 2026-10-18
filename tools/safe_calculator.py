
import ast
import operator

from langchain_core.tools import tool


# Only allow basic mathematical operations.
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node):
    """Evaluate a restricted arithmetic expression."""

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(
            node.value, bool
        ):
            return node.value

        raise ValueError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp):
        operator_type = type(node.op)

        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("This operator is not allowed.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        # Prevent excessive exponentiation.
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent is too large.")

        return _ALLOWED_OPERATORS[operator_type](left, right)

    if isinstance(node, ast.UnaryOp):
        operator_type = type(node.op)

        if operator_type not in _ALLOWED_OPERATORS:
            raise ValueError("This unary operator is not allowed.")

        return _ALLOWED_OPERATORS[operator_type](
            _evaluate(node.operand)
        )

    raise ValueError("Invalid or unsafe mathematical expression.")


@tool
def safe_calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression safely.

    Supports addition, subtraction, multiplication, division,
    floor division, modulo, powers, and parentheses.
    """

    try:
        parsed_expression = ast.parse(expression, mode="eval")
        result = _evaluate(parsed_expression.body)
        return str(result)

    except (SyntaxError, ValueError, TypeError, ZeroDivisionError,
            OverflowError) as error:
        return f"Calculation error: {error}"
