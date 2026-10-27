
from app.services.answer_service import AnswerService
from app.services.search_service import SearchService


if __name__ == "__main__":
    question = "How much attendance is required for examinations?"

    search_service = SearchService()
    results = search_service.search(question, top_k=3)

    answer_service = AnswerService()
    answer = answer_service.generate_answer(question, results)

    print("\nQUESTION:")
    print(question)

    print("\nGENERATED ANSWER:")
    print(answer)

    print("\nRETRIEVED SOURCES:")
    for index, result in enumerate(results, start=1):
        print(
            f"[S{index}] {result['document_name']}, "
            f"page {result['page_number']}"
        )
