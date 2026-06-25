
import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.core.config import get_settings


def generate_answer(state):
    print("==== generate answer agent====")

    settings = get_settings()

    llm = ChatOpenAI(
        model=settings.openai_chat_model,
        api_key=settings.open_api_key,
        temperature=0,
    )

    question = state["user_question"]

    chunks = state.get("retrieved_chunks", [])

    if not chunks:
        return {
            "draft_answer": None,
            "answer_is_supported": False,
        }

    if isinstance(chunks, str):
        chunks = json.loads(chunks)

    context_text = "\n\n".join([
        f"[{c['document_name']} - page {c['page_number']}]\n{c['chunk_text']}"
        for c in chunks
    ])

    system_prompt = SystemMessage(
        content="""
            You are a strict policy assistant.

            You MUST:
            - Answer ONLY using the provided context
            - NEVER use external knowledge
            - NEVER assume missing information
            - NEVER fabricate policies

            If the answer is not clearly supported by the context, respond EXACTLY with:
            "I could not find this information in the uploaded policy documents."

            NOT burn more than 100 tokens
        """
    )

    user_prompt = HumanMessage(
        content=f"""
            Question:
            {question}

            Context:
            {context_text}

            Provide a clear and concise answer with references.
        """
    )

    response = llm.invoke([system_prompt, user_prompt])

    answer = response.content.strip()

    is_supported = "I could not find" not in answer

    return {
        "draft_answer": answer,
        "answer_is_supported": is_supported,
    }





