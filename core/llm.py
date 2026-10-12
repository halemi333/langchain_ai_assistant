from langchain_openai import ChatOpenAI

from core.config import OPENAI_API_KEY

llm = ChatOpenAI(

    model="gpt-4.1-mini",

    temperature=0,

    api_key=OPENAI_API_KEY

)