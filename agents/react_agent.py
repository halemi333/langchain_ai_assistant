
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from core.llm import llm
from memory.memory import memory


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an analytical AI assistant.

Your responsibilities:
- Analyze complex questions carefully.
- Explain the reasons behind your conclusions.
- Compare alternatives when appropriate.
- Organize the response into clear sections.
- Produce structured, useful reports in the user's language.
- Clearly distinguish facts, assumptions, and recommendations.
- Do not claim to have accessed live information or external
  sources unless that information was provided in the conversation.

You must not call tools or perform external actions.
"""
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)


chain = prompt | llm | StrOutputParser()


def run_react_agent(user_input: str) -> str:

    history = memory.load_memory_variables({})["chat_history"]

    response = chain.invoke(
        {
            "input": user_input,
            "chat_history": history
        }
    )

    memory.save_context(
        {"input": user_input},
        {"output": response}
    )

    return response
