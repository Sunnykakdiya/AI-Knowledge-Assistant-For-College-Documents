
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.search_service import SearchService
from app.services.answer_service import AnswerService

router = APIRouter(prefix="/api/v1", tags=["Question Answering"])


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=10)


class SearchResult(BaseModel):
    document_name: str
    page_number: int | None
    text: str
    similarity: float


class QuestionResponse(BaseModel):
    question: str
    results: list[SearchResult]


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SearchResult]


@router.post("/search", response_model=QuestionResponse)
def search_documents(request: QuestionRequest):
    try:
        results = SearchService().search(
            request.question,
            request.top_k,
        )
        return QuestionResponse(
            question=request.question,
            results=[
                SearchResult(
                    document_name=r["document_name"],
                    page_number=r["page_number"],
                    text=r["text"],
                    similarity=r["similarity"],
                )
                for r in results
            ],
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Document search failed. Check server logs.",
        ) from error


@router.post("/ask", response_model=AskResponse)
def ask_question(request: QuestionRequest):
    try:
        results = SearchService().search(
            request.question,
            request.top_k,
        )

        answer = AnswerService().generate_answer(
            request.question,
            results,
        )

        return AskResponse(
            question=request.question,
            answer=answer,
            sources=[
                SearchResult(
                    document_name=r["document_name"],
                    page_number=r["page_number"],
                    text=r["text"],
                    similarity=r["similarity"],
                )
                for r in results
            ],
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Answer generation failed. Check server logs.",
        ) from error
