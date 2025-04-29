from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chatbot import get_llm_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = get_llm_response(request.message)
    return ChatResponse(response=response)