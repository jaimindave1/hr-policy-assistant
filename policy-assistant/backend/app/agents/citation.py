import json


def generate_citations(state):
    print("==== citation agent====")

    chunks = state.get("retrieved_chunks", [])

    seen = set()
    citations = []

    if isinstance(chunks, str):
        chunks = json.loads(chunks)

    for c in chunks:
        key = (c["document_name"], c["page_number"])

        if key not in seen:
            seen.add(key)

            citations.append({
                "document": c["document_name"],  
                "page": c["page_number"],       
                "chunk_id": c["chunk_id"],
            })
    return {
        "citations": citations
    }
