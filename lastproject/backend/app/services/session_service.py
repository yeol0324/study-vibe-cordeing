"""세션 관리 서비스"""
from typing import Optional, Dict, Any
from datetime import datetime

from app.agent_memory import memory_agent
from app.models.session import SessionModel
from app.models.chat import MultiturnChatResponse, MessageHistory


class SessionService:
    """세션 관리 서비스 클래스"""
    
    def __init__(self):
        """세션 서비스 초기화"""
        self.memory_agent = memory_agent
        
    def create_or_get_session(self, user_id: str, session_id: Optional[str]) -> SessionModel:
        """세션 생성 또는 조회"""
        if session_id:
            # 기존 세션 조회
            session = self.memory_agent.get_session(session_id)
            if session and session.user_id == user_id:
                return session
        
        # 새 세션 생성
        return self.memory_agent.create_session(user_id)
        
    def get_chat_config(self, session: SessionModel) -> Dict[str, Any]:
        """채팅 설정 생성"""
        return {
            "configurable": {
                "thread_id": session.thread_id,
                "user_id": session.user_id
            }
        }
        
    def save_user_message_memory(self, user_id: str, message: str):
        """사용자 메시지 메모리 저장"""
        memory_data = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "type": "user_message",
            "role": "user"
        }
        return self.memory_agent.memory_system.save_user_memory(user_id, memory_data)
        
    def save_assistant_response_memory(self, user_id: str, response: str):
        """어시스턴트 응답 메모리 저장"""
        memory_data = {
            "message": response,
            "timestamp": datetime.now().isoformat(),
            "type": "assistant_response", 
            "role": "assistant"
        }
        return self.memory_agent.memory_system.save_user_memory(user_id, memory_data)
        
    def process_message(self, user_id: str, message: str, session_id: Optional[str]) -> MultiturnChatResponse:
        """메시지 처리"""
        # 세션 생성 또는 조회
        session = self.create_or_get_session(user_id, session_id)
        
        # 에이전트 그래프 생성
        agent_graph = self.memory_agent.create_agent_graph()
        
        # 채팅 설정 생성
        config = self.get_chat_config(session)
        
        # 사용자 메시지 메모리 저장
        self.save_user_message_memory(user_id, message)
        
        # 에이전트 실행
        result = agent_graph.invoke({
            "messages": [{"role": "user", "content": message}]
        }, config)
        
        # 응답 추출
        if result and "messages" in result and len(result["messages"]) > 0:
            response_text = result["messages"][-1].content
        else:
            response_text = "죄송합니다. 응답을 생성할 수 없습니다."
            
        # 어시스턴트 응답 메모리 저장
        self.save_assistant_response_memory(user_id, response_text)
        
        # 대화 히스토리 조회
        message_history = self.get_message_history(user_id, limit=10)
        
        return MultiturnChatResponse(
            response=response_text,
            session_id=session.session_id,
            thread_id=session.thread_id,
            message_history=message_history
        )
        
    def get_message_history(self, user_id: str, limit: int = 10) -> list[MessageHistory]:
        """메시지 히스토리 조회"""
        memories = self.memory_agent.memory_system.search_user_memories(user_id, limit=limit)
        
        # 메시지 타입 메모리만 필터링하고 시간순 정렬
        message_memories = [
            memory for memory in memories 
            if memory.get("type") in ["user_message", "assistant_response"]
        ]
        
        # 타임스탬프로 정렬
        message_memories.sort(key=lambda x: x.get("timestamp", ""))
        
        # MessageHistory 객체로 변환
        history = []
        for memory in message_memories[-limit:]:  # 최근 limit개만
            history.append(MessageHistory(
                role=memory.get("role", "user"),
                content=memory.get("message", ""),
                timestamp=memory.get("timestamp", "")
            ))
            
        return history


# 전역 세션 서비스 인스턴스
session_service = SessionService() 