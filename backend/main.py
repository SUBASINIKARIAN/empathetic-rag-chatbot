import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from claude_client import chat

app = FastAPI(title="Empathetic RAG Chatbot API")

sessions: dict[str, list[dict]] = {}
feedback_log: list[dict] = []


class ChatRequest(BaseModel):
    session_id: str
    message: str


class FeedbackRequest(BaseModel):
    session_id: str
    message_id: str
    rating: int  # 1 = thumbs up, 0 = thumbs down


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if req.session_id not in sessions:
        sessions[req.session_id] = []

    history = sessions[req.session_id]
    result = chat(req.message, history, req.session_id)
    sessions[req.session_id] = history
    return result


@app.post("/feedback")
async def feedback_endpoint(req: FeedbackRequest):
    if req.rating not in (0, 1):
        raise HTTPException(status_code=400, detail="Rating must be 0 or 1")
    feedback_log.append({
        "session_id": req.session_id,
        "message_id": req.message_id,
        "rating": req.rating,
        "timestamp": datetime.now().isoformat(),
    })
    return {"status": "recorded"}


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    sessions.pop(session_id, None)
    return {"status": "cleared"}


@app.get("/health")
async def health():
    return {"status": "ok", "sessions_active": len(sessions)}
