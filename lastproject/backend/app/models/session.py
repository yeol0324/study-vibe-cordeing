"""사용자 세션 모델"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionModel(BaseModel):
    """세션 데이터 모델"""
    session_id: str
    user_id: str
    thread_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    @classmethod
    def create_new_session(cls, user_id: str) -> "SessionModel":
        """새 세션 생성"""
        session_id = str(uuid.uuid4())
        thread_id = str(uuid.uuid4())
        return cls(
            session_id=session_id,
            user_id=user_id,
            thread_id=thread_id
        )


class SessionRequest(BaseModel):
    """세션 기반 채팅 요청 모델"""
    message: str
    user_id: str
    session_id: Optional[str] = None  # None이면 새 세션 생성


class SessionResponse(BaseModel):
    """세션 기반 채팅 응답 모델"""
    response: str
    session_id: str
    thread_id: str 