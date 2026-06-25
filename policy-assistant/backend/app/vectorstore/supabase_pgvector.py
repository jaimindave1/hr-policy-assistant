
from typing import List
import psycopg
from app.core.config import get_settings
from app.core.app_logging import get_logger

logger = get_logger(__name__)

class SupabasePGVectorStore:
    """
    Handles pgvector operations (insert + search)
    """

    def __init__(self) -> None:
        settings = get_settings()
        self.connection_string = settings.supabase_db_url

    def get_connection(self):
        return psycopg.connect(self.connection_string, connect_timeout=10)
    
    def insert_chunks(self, chunks: List[dict]):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                for chunk in chunks:
                    cur.execute(
                        """
                        insert into policy_chunks (id, document_name, page_number, chunk_text, embeddings)
                        values (%s, %s, %s, %s, %s)
                        """,
                        (
                           chunk["chunk_id"], 
                           chunk["document_name"],
                           chunk["page_number"],
                           chunk["chunk_text"],
                           chunk["embeddings"]
                        )
                    )
    
            conn.commit()

            logger.info("Chunks inserted successfully")

    def to_pgvector(self, vec: list[float]) -> str:
        return "[" + ",".join(str(x) for x in vec) + "]"

    def similarity_search(self, query_embeddings: list[float], top_k: int = 500):

        embedding_str = "[" + ",".join(map(str, query_embeddings)) + "]"

        # query = """
        # select
        # id,
        # document_name,
        # page_number,
        # chunk_text,
        # 1 - (embeddings <=> %s::vector) as similarity_score
        # from policy_chunks
        # order by (embeddings <=> %s::vector)
        # limit 10;
        # """

        query = """
        WITH ranked AS (
            SELECT
                id,
                document_name,
                page_number,
                chunk_text,
                1 - (embeddings <=> %s::vector) AS sim
            FROM policy_chunks
        )
        SELECT *
        FROM ranked
        WHERE sim > 0.1
        ORDER BY sim DESC
        LIMIT 10;
        """

        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (embedding_str,))
                rows = cur.fetchall()

        print(f"Rows returned: {len(rows)}")

        for r in rows:
            print(
                "similarity:", r[4],
                "| text:", r[3][:100]
            )

        return [
            {
                "chunk_id": str(row[0]),
                "document_name": row[1],
                "page_number": row[2],
                "chunk_text": row[3],
                "similarity_score": float(row[4]),
            }
            for row in rows
        ]





