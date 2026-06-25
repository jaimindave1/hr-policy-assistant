from typing import Annotated, TypedDict, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class RetrievedChunk(TypedDict):
    f"""
    A single retrieved policy document chunk from Supabase pgvector.

    This is intentionally small and directly aligned with what we store
    in the vector database.
    """
    chunk_id: str
    document_name: str
    page_number: int | None
    chunk_text: str
    similarity_score: float


class Citation(TypedDict):
    """
    Source reference shown to the user.

    The answer must cite the policy documents that support it.
    """

    document_name: str
    page_number: int | None
    chunk_id: str


class PolicyAssistantState(TypedDict):
    f"""
    Shared LangGraph state for one policy assistant chat request.

    Each graph node receives this state and returns a partial update.
    LangGraph merges the updates between nodes.
    """

    # Conversation messages.
    #
    # add_messages tells LangGraph to append new messages instead of
    # replacing the entire list.
    messages: Annotated[list[BaseMessage], add_messages]

    # Raw user question from the API request.
    user_question: str

    # Query rewritten or normalized by the Query Analysis Agent.
    retrieval_query: str

    # Chunks retrieved from Supabase pgvector.
    retrieved_chunks: list[RetrievedChunk]

    # Whether the retrieved context is sufficient to answer.
    context_is_relevant: bool

    # Reason why context is considered insufficient.
    relevance_reason: str | None

    # Draft answer produced by the Answer Generation Agent.
    draft_answer: str | None

    # Final citations attached to the answer.
    citations: list[Citation]

    # Whether the final response is allowed to be returned.
    answer_is_supported: bool

    # Guardrail decision.
    guardrail_status: Literal["allowed", "blocked"]

    # Final answer returned to the API.
    final_answer: str