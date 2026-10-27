
from app.services.ingestion_service import IngestionService

if __name__ == "__main__":
    service = IngestionService()

    pdf_path = "data/documents/sample_college_policy.pdf"

    try:
        count = service.ingest_pdf(pdf_path)
        print("SUCCESS: PDF ingestion completed!")
        print("Chunks inserted:", count)
    except Exception as error:
        print("INGESTION FAILED")
        print(type(error).__name__ + ":", error)
