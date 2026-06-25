
from app.vectorstore.supabase_pgvector import SupabasePGVectorStore
from typing import List

class DocumentRepository:
    """
    Thin layer over vector store.
    """

    def __init__(self) -> None:
        self.vector_store = SupabasePGVectorStore()

    def save_chunks(self, chunks: List[dict]) -> None:
        self.vector_store.insert_chunks(chunks)

    def search_chunks(
        self,
        query_embedding: list[float],
        top_k: int,
        ) -> List[dict]:
        return self.vector_store.similarity_search(query_embedding, top_k)