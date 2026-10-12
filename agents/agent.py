from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from prompts.agent_prompt import prompt

from core.llm import llm
from memory.memory import memory

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


agent = create_tool_calling_agent(

    llm,

    tools,

    prompt

)

agent_executor = AgentExecutor(

    agent=agent,

    tools=tools,
    
    memory=memory,
     
    verbose=True

)

def run_agent(user_input):

    response = agent_executor.invoke(

        {
            "input": user_input
        }

    )

    return response["output"]