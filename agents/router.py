from core.llm import llm

from agents.agent import run_agent

from agents.react_agent import run_react_agent

def route_request(user_input):

    prompt = f"""
You are a router.

Decide which agent should handle the request.

Available agents:

1. normal_agent:
For simple tasks like:
- calculations
- saving notes
- creating tasks

2. react_agent:
For complex tasks requiring reasoning,
analysis, multiple steps.

User request:

{user_input}

Return only one word:

normal
or
react
"""

    response = llm.invoke(
        prompt
    )

    decision = response.content.strip()

    if decision == "react":

        return run_react_agent(
            user_input
        )

    else:

        return run_agent(
            user_input
        )