from langchain.agents import (
    AgentExecutor,
    create_react_agent
)

from langchain import hub

from core.llm import llm

from tools.calculator import calculator
from tools.notes import (
    save_note,
    get_notes
)
from tools.tasks import (
    add_task,
    list_tasks
)

tools = [

    calculator,

    save_note,

    get_notes,

    add_task,

    list_tasks

]

prompt = hub.pull(
    "hwchase17/react"
)

agent = create_react_agent(

    llm,

    tools,

    prompt

)

agent_executor = AgentExecutor(

    agent=agent,

    tools=tools,

    verbose=True

)

def run_react_agent(user_input):

    response = agent_executor.invoke(

        {
            "input": user_input
        }

    )

    return response["output"]