
from app.services.search_service import SearchService

if __name__ == "__main__":
    service = SearchService()

    question = "How much attendance is required for examinations?"
    results = service.search(question, top_k=3)

    print("Question:", question)
    print("Results found:", len(results))

    for result in results:
        print("\nDocument:", result["document_name"])
        print("Page:", result["page_number"])
        print("Similarity:", round(result["similarity"], 4))
        print("Text:", result["text"])
