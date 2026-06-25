from typing import List
from langchain_openai import OpenAIEmbeddings
from app.core.config import get_settings
from app.core.app_logging import get_logger
import numpy as np

logger = get_logger(__name__)
def normalize(v):
    return v / np.linalg.norm(v)

class EmbeddingService:
    """
    Handles OpenAI embedding generation.
    """

    def __init__(self) -> None:
            settings = get_settings()

            self.model_name = settings.openai_embedding_model

            self.embeddings = OpenAIEmbeddings(
                model=self.model_name,
                api_key=settings.open_api_key,
            )


    def embed_chunks(self, chunks: List[dict]) -> List[dict]:
        """
        Adds embeddings to chunk objects.

        Input:
            [
                { chunk_id, chunk_text, ... }
            ]

        Output:
            [
                { ..., embeddings: [...] }
            ]
        """


        if not chunks:
            return []
        
        logger.info("Generating embeddings", total_chunks=len(chunks))

        texts = [c["chunk_text"] for c in chunks]

        vectors = self.embeddings.embed_documents(texts)

        vectors = [normalize(v) for v in vectors]
        vectors = [v.tolist() for v in vectors]  

        enriched_chunks = []

        for chunk, vector in zip(chunks, vectors):
            enriched = {
                **chunk,
                "embeddings": vector,
            }
            enriched_chunks.append(enriched)

        logger.info(f"Embeddings generated {enriched_chunks}")

        return enriched_chunks



