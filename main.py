
from fastapi import FastAPI

app = FastAPI(
    title="College Knowledge Assistant",
    description="An API for answering questions about college documents.",
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
