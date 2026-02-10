import os
import time
import httpx
from fastapi import FastAPI, Request, BackgroundTasks 
from fastapi.responses import JSONResponse

from src.domain.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService
from src.core.logger import get_logger
from src.core.config import settings 

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

app = FastAPI(
    title="Braite AI - BPJS Chatbot Engine",
    description="Enterprise Grade Chatbot Backend with RAG & Webhook Integration",
    version="1.0.0"
)

logger = get_logger("API_Gateway")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

try:
    logger.info("Booting up Chat Service...")
    chat_service = ChatService()
    logger.info("Chat Service is Ready!")
except Exception as e:
    logger.error(f"CRITICAL ERROR: Failed to start Chat Service. {e}")
    raise e

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        # Log hanya jika request sukses
        if response.status_code == 200:
            logger.info(f"Handled {request.method} {request.url.path} in {process_time:.2f}s")
        return response
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

async def process_telegram_message(chat_id: str, text: str, username: str):
    logger.info(f"Processing BG Task for {username}: {text[:30]}...")
    
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendChatAction",
                json={"chat_id": chat_id, "action": "typing"}
            )

        ai_response = chat_service.generate_response(
            query=text,
            session_id=f"tg-{chat_id}"
        )

        await send_telegram_message(chat_id, ai_response.answer)
        
        if ai_response.sources:
            source_text = "\n📚 *Sumber Referensi:*\n" + "\n".join([f"• {s}" for s in ai_response.sources])
            await send_telegram_message(chat_id, source_text)
            
        logger.info(f"BG Task Finished for {username}")

    except Exception as e:
        logger.error(f"Background Task Error: {e}")
        await send_telegram_message(chat_id, "Maaf, sistem sedang sibuk. Silakan coba lagi.")

async def send_telegram_message(chat_id: str, text: str):
    """Mengirim pesan balik ke server Telegram"""
    async with httpx.AsyncClient() as client:
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown" 
        }
        try:
            await client.post(TELEGRAM_API_URL, json=payload, timeout=10.0)
        except Exception as e:
            logger.error(f"Failed to send to Telegram: {e}")

@app.get("/", tags=["General"])
async def root():
    return {"status": "online", "service": "Braite BPJS Chatbot"}

@app.post("/chat", response_model=ChatResponse, tags=["Core AI"])
async def chat_endpoint(request: ChatRequest):
    response = chat_service.generate_response(request.query, request.session_id)
    return response

@app.post("/webhook/telegram", tags=["Integrations"])
async def telegram_webhook(payload: dict, background_tasks: BackgroundTasks):
    try:
        if "message" not in payload:
            return {"status": "ignored"}
            
        message_data = payload["message"]
        text = message_data.get("text", "")
        chat_id = str(message_data["chat"]["id"])
        username = message_data["chat"].get("username", "Unknown")
        
        if not text:
            return {"status": "ok"}
        background_tasks.add_task(process_telegram_message, chat_id, text, username)

        return {"status": "received"}

    except Exception as e:
        logger.error(f"Webhook Handler Error: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)