from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.schemas import ChatRequest
from app.services.chat_service import ChatService
from fastapi.responses import StreamingResponse
from starlette.responses import Response


router = APIRouter(prefix="/chat", tags=["chat"])

chat_service = ChatService()


@router.post("/stream")
async def stream_chat(request: ChatRequest):
    """
    Streaming chat endpoint.
    """

    try:
        generator = chat_service.stream_chat(request.message)
        
        return StreamingResponse(
            generator,
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Transfer-Encoding": "chunked",
            },
        )


    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chat processing failed.",
        )

@router.get("/status")
def chat_status() -> dict[str, str]:
    return {"status": "chat API placeholder"}
