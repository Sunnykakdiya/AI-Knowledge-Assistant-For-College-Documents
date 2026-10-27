
from fastapi import FastAPI

from app.api.qa import router as qa_router
from app.api.documents import router as documents_router

app = FastAPI(
    title="College Knowledge Assistant",
    description="Ask questions about uploaded college documents.",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "College Knowledge Assistant API is running!",
        "status": "success",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(qa_router)
app.include_router(documents_router)
