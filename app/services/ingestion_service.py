
from pathlib import Path

from sqlalchemy import text

from app.db.session import engine
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import chunk_text
from app.services.embedding_service import EmbeddingService


class IngestionService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def ingest_pdf(self, pdf_path: str) -> int:
        path = Path(pdf_path)

        pages = extract_text_from_pdf(str(path))

        if not pages:
            raise ValueError(
                "No extractable text found in the PDF."
            )

        records = []

        for page in pages:
            chunks = chunk_text(page["text"])

            for chunk in chunks:
                records.append({
                    "document_name": path.name,
                    "page_number": page["page_number"],
                    "chunk_text": chunk,
                })

        if not records:
            raise ValueError("No text chunks were generated.")

        vectors = self.embedding_service.embed_texts(
            [record["chunk_text"] for record in records]
        )

        insert_sql = text("""
            INSERT INTO document_chunks
                (document_name, page_number, chunk_text, embedding)
            VALUES
                (:document_name, :page_number, :chunk_text,
                 CAST(:embedding AS vector))
        """)

        for record, vector in zip(records, vectors):
            record["embedding"] = "[" + ",".join(
                str(value) for value in vector
            ) + "]"

        with engine.begin() as connection:
            connection.execute(insert_sql, records)

        return len(records)
