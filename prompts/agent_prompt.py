from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(

    [

        (
            "system",
            "You are a helpful AI assistant."
        ),

        (
            "placeholder",
            "{chat_history}"
        ),

        (
            "human",
            "{input}"
        ),

        (
            "placeholder",
            "{agent_scratchpad}"
        )

    ]

)