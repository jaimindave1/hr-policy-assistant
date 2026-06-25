from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from app.core.config import get_settings
from app.agents.tools import retrieval_tool

def create_query_analysis_agent():
    print("==== query analysis agent====")
    settings = get_settings()

    llm = ChatOpenAI(
        model = settings.openai_chat_model,
        api_key=settings.open_api_key,
        temperature=0
    )

    agent = create_react_agent(
        llm,
        tools=[retrieval_tool]
    )
    
    return agent
