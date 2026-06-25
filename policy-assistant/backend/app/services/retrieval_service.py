
from typing import List

from app.core.config import get_settings
from app.core.app_logging import get_logger
from app.repositories.document_repository import DocumentRepository
from app.services.embedding_service import EmbeddingService
import numpy as np


def normalize(v):
    return v / np.linalg.norm(v)

logger = get_logger(__name__)

class RetrievalService:
    """
    Handles semantic search over policy documents.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.embedding_service = EmbeddingService()
        self.repository = DocumentRepository()

    def retrieve(self, query: str) -> List[dict]:
        """
        Perform semantic retrieval based on user query.
        """

        if not query.strip():
            return []

        logger.info("Retrieval started", query=query)

        query_embedding = self.embedding_service.embeddings.embed_query(query)

        query_embedding = normalize(query_embedding)

        logger.info(f"query_embedding==={query_embedding}")

        results = self.repository.search_chunks(
            query_embedding=query_embedding,
            top_k=self.settings.retrieval_top_k,
        )

        filtered = [
            r for r in results
            if r["similarity_score"] >= self.settings.relevance_threshold
        ]

        logger.info(
            "Retrieval completed",
            total=len(results),
            filtered=len(filtered),
        )

        return filtered

