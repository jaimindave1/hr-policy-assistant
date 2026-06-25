from typing import Literal
from langgraph.graph import END, START, StateGraph
from app.graphs.state import PolicyAssistantState
from app.core.app_logging import get_logger
from app.services.retrieval_service import RetrievalService
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from app.agents.query_analysis import create_query_analysis_agent
from langgraph.prebuilt import ToolNode
from app.agents.tools import retrieval_tool
from app.agents.answer_generation import generate_answer
from app.agents.citation import generate_citations
from app.agents.guardrail import apply_guardrail
from app.utils.debug import print_messages

logger = get_logger(__name__)

graph = StateGraph(PolicyAssistantState)

retrieval_service = RetrievalService()

def agent_node(state: PolicyAssistantState):
    agent = create_query_analysis_agent()

    system_prompt=SystemMessage(content=f"""
    You are a query assitant agent. You MUST answer the query using company policy documents.

    Rules:
    - you MUST use the retrieval tool to get the information
    - Do NOT answer from memory
    - Do NOT make assumptions
    - If no relevant information found, say:
        "I could not find the related information from the company policy documents."
    - Dont burn more than 100 tokens.
    """
    )

    messages = [system_prompt] + state["messages"]

    print_messages(messages, title="Agent Execution")

    result = agent.invoke({"messages": messages})

    messages = result["messages"]

    print_messages(messages, title="Agent Invoked and appended to messages")

    retrieved_chunks = []

    for msg in messages:
        if hasattr(msg, "name") and msg.name == "retrieval_tool":
            retrieved_chunks = msg.content

    return {
        "messages": messages,
        "retrieved_chunks": retrieved_chunks,
    }

def query_analysis(state: PolicyAssistantState):
    f"""
    Converts user question in to retrieval query
    """

    logger.info("Running Query Analysis Node")

    user_question = state.get("user_question")

    return {
        "retrieval_query": user_question
    }

def retrieval(state: PolicyAssistantState):
    f"""
    Retrieves chunks from vector db
    """

    logger.info("Running Retrieval Node")
    
    query = state.get("retrieval_query", "")

    results = retrieval_service.retrieve(query)

    return {
        "retrieved_chunks": results
    }

def relevance_validation_node(state: PolicyAssistantState) -> dict:
    """
    Determines if retrieved chunks are sufficient.
    """
    logger.info("Running Relevance Validation Node")

    chunks = state.get("retrieved_chunks", [])

    if not chunks:
        return {
            "context_is_relevant": False,
            "relevance_reason": "No chunks retrieved",
        }

    # max_score = max([c["similarity_score"] for c in chunks])

    # if max_score < 0.75:
    #     return {
    #         "context_is_relevant": False,
    #         "relevance_reason": f"Low confidence context (max_score={max_score})",
    #     }
    
    return {
        "context_is_relevant": True,
        "relevance_reason": None,
    }

def route_after_relevance(state: PolicyAssistantState) -> Literal["answer_generation", "guardrail"]:
    """
    Decide next step after relevance validation.
    """
    if not state.get("context_is_relevant", False):
        return "guardrail"

    return "answer_generation"

def route_agent(state: PolicyAssistantState):
    last_msg = state["messages"][-1]

    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"

    if state.get("retrieved_chunks"):
        return "relevance_validation"
    
    return "guardrail"

def build_graph():
    """
    Creates and compiles the LangGraph workflow.
    """

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode([retrieval_tool]))
    graph.add_node("relevance_validation", relevance_validation_node)
    graph.add_node("answer_generation", generate_answer)
    graph.add_node("citation", generate_citations)
    graph.add_node("guardrail", apply_guardrail)

    graph.add_edge(START,"agent")
    
    graph.add_conditional_edges(
        "agent",
        route_agent,
        {
            "tools": "tools",
            "relevance_validation": "relevance_validation",
            "guardrail": "guardrail",
        },
    )

    # After tool execution → go back to agent
    graph.add_edge("tools", "agent")
    graph.add_edge("tools", "relevance_validation")
   
    graph.add_conditional_edges(
        "relevance_validation",
        route_after_relevance,
        {
            "answer_generation": "answer_generation",
            "guardrail": "guardrail",
        },
    )

    graph.add_edge("answer_generation", "citation")
    graph.add_edge("citation", "guardrail")
    graph.add_edge("guardrail", END)

    return graph.compile()