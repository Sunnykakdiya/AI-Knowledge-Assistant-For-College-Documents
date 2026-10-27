
from sqlalchemy import text

from app.db.session import engine


def setup_database():
    with engine.begin() as connection:
        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector;")
        )

        connection.execute(
            text("""
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id BIGSERIAL PRIMARY KEY,
                    document_name TEXT NOT NULL,
                    chunk_text TEXT NOT NULL,
                    embedding VECTOR(384),
                    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                );
            """)
        )

        connection.execute(
            text("""
                CREATE INDEX IF NOT EXISTS
                idx_document_chunks_embedding
                ON document_chunks
                USING hnsw (embedding vector_cosine_ops);
            """)
        )

    print("SUCCESS: pgvector extension is enabled.")
    print("SUCCESS: document_chunks table is ready.")
    print("SUCCESS: vector search index is ready.")


if __name__ == "__main__":
    setup_database()
