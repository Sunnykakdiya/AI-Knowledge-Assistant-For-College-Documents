
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.ingestion_service import IngestionService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)

UPLOAD_DIR = Path("data/documents")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted.",
        )

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    saved_path = UPLOAD_DIR / f"{uuid4().hex}.pdf"

    try:
        # Read at most 50 MB + 1 byte to detect oversized uploads.
        content = await file.read(MAX_FILE_SIZE + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty.",
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="PDF exceeds the 50 MB upload limit.",
            )

        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=400,
                detail="The uploaded file does not have a valid PDF header.",
            )

        saved_path.write_bytes(content)

        # Extract text, create chunks and embeddings, then save to PostgreSQL.
        chunks_inserted = IngestionService().ingest_pdf(str(saved_path))

        logger.info(
            "PDF processed successfully: %s (%s chunks)",
            file.filename,
            chunks_inserted,
        )

        return {
            "message": "PDF processed successfully.",
            "document_id": saved_path.stem,
            "original_filename": file.filename,
            "file_size_mb": round(len(content) / (1024 * 1024), 2),
            "chunks_inserted": chunks_inserted,
        }

    except HTTPException:
        saved_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        # Print the complete traceback in the FastAPI terminal.
        logger.exception(
            "PDF processing failed for uploaded file: %s",
            file.filename,
        )
        saved_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=(
                "PDF processing failed. Check the FastAPI terminal "
                "for the detailed error."
            ),
        ) from error

    finally:
        await file.close()
