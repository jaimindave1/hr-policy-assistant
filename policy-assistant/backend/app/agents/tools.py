from typing import List

from langchain_core.tools import tool

from app.services.retrieval_service import RetrievalService

retrieval_service = RetrievalService()

@tool()
def retrieval_tool(query: str) -> List[dict]:
    """
    Retrieve relevant policy document chunks based on a query.

    This is the ONLY allowed tool.
    """
    print("==== retrieval tool agent====")

    chunks = retrieval_service.retrieve(query)

    return chunks