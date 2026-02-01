from typing import List, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Pertanyaan user terkait BPJS")
    session_id: str = Field(..., description="ID unik session (misal: UUID) untuk memori percakapan")

class ChatResponse(BaseModel):
    answer: str = Field(..., description="Jawaban dari AI")
    sources: List[str] = Field(default=[], description="Daftar dokumen referensi yang digunakan")