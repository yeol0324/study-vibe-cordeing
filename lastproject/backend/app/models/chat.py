from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str


class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str


class MessageHistory(BaseModel):
    """메시지 히스토리 모델"""
    role: str  # "user" 또는 "assistant"
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class MultiturnChatRequest(BaseModel):
    """멀티턴 채팅 요청 모델"""
    message: str
    user_id: str
    session_id: Optional[str] = None  # None이면 새 세션 생성


class MultiturnChatResponse(BaseModel):
    """멀티턴 채팅 응답 모델"""
    response: str
    session_id: str
    thread_id: str
    message_history: List[MessageHistory] = [] 