FALLBACK = "I could not find this information in the policy documents."

def apply_guardrail(state):
    print("==== guard rail agent====")
    chunks = state.get("retrieved_chunks", [])
    draft = state.get("draft_answer")
    citations = state.get("citations")
    state["citations"] = []
    if not chunks:
        return {
            "guardrail_status": "blocked",
            "final_answer": FALLBACK,
        }

    
    if not draft:
        return {
            "guardrail_status": "blocked",
            "final_answer": FALLBACK,
        }

    return {
        "guardrail_status": "allowed",
        "final_answer": draft,
        "citations": citations
    }