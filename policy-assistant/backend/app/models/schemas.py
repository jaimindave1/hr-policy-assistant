from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"
    app_name: str

class ErrorResponse(BaseModel):
    detail: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)

class SourceCitation(BaseModel):
    document_name: str
    page_number: int | None = None
    chunk_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceCitation] = Field(default_factory=list)
