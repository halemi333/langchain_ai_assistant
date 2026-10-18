
from tools.safe_calculator import safe_calculator

result = safe_calculator.invoke({
    "expression": "2 + 3 * 4"
})
print("Valid expression:", result)

result = safe_calculator.invoke({
    "expression": "__import__('os').getcwd()"
})
print("Unsafe expression:", result)
