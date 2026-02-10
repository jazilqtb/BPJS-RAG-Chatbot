import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.domain.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.core.config import settings 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chat = ChatService()

@app.post("/chat")
async def handle_bpjs_chat(request: ChatRequest) -> ChatResponse:
    response = chat.generate_response(query=request.query, session_id=request.session_id)
    return response