
from sqlalchemy import text

from app.db.session import engine
from app.services.embedding_service import EmbeddingService


class SearchService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not query.strip():
            raise ValueError("Search query cannot be empty.")

        if top_k < 1:
            raise ValueError("top_k must be at least 1.")

        query_vector = self.embedding_service.embed_query(query)
        vector_string = "[" + ",".join(
            str(value) for value in query_vector
        ) + "]"

        sql = text("""
            SELECT
                id,
                document_name,
                page_number,
                chunk_text,
                1 - (embedding <=> CAST(:query_vector AS vector))
                    AS similarity
            FROM document_chunks
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:query_vector AS vector)
            LIMIT :top_k
        """)

        with engine.connect() as connection:
            rows = connection.execute(
                sql,
                {
                    "query_vector": vector_string,
                    "top_k": top_k,
                },
            ).mappings().all()

        return [
            {
                "id": row["id"],
                "document_name": row["document_name"],
                "page_number": row["page_number"],
                "text": row["chunk_text"],
                "similarity": float(row["similarity"]),
            }
            for row in rows
        ]
