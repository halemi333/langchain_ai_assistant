from core.llm import llm

from agents.agent import run_agent
from agents.react_agent import run_react_agent


def route_request(user_input: str) -> str:

    if not user_input.strip():
        return "Please enter a request."

    prompt = f"""
You are a request classifier.

Your job is ONLY to choose which agent should handle
the user's request. Do not answer the request.

Available agents:

1. normal
Choose normal for simple tasks supported by the
available tools, such as:
- Basic calculations
- Saving or retrieving notes
- Adding or listing tasks
- Simple, direct requests

2. react
Choose react for:
- Complex reasoning and analysis
- Multi-step tasks
- Comparing multiple options
- Combining information from different sources
- Research and detailed report preparation
- Tasks requiring planning and several actions

Rules:
- Choose based on the overall task.
- Do not execute the task.
- Return exactly one word: normal or react.
- Do not include explanations.

User request:
<user_request>
{user_input}
</user_request>

Agent:
"""

    # Step 1: Ask the LLM to classify the request.
    try:
        response = llm.invoke(prompt)
        decision = response.content.strip().lower()

    except Exception as error:
        return f"Router Error: Could not classify the request: {error}"

    # Step 2: Validate the classification.
    if decision not in ("normal", "react"):
        return (
            "Router Error: Invalid agent selection. "
            f"Received: {decision!r}"
        )

    # Step 3: Execute the selected agent.
    try:
        if decision == "normal":
            return run_agent(user_input)

        return run_react_agent(user_input)

    except Exception as error:
        return f"Agent Execution Error: {error}"