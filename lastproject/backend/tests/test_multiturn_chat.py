"""멀티턴 채팅 모델 테스트"""
import pytest
from app.models.chat import MultiturnChatRequest, MultiturnChatResponse, MessageHistory


class TestMultiturnChatModels:
    """멀티턴 채팅 모델 테스트 클래스"""
    
    def test_message_history_model(self):
        """메시지 히스토리 모델 테스트"""
        message = MessageHistory(
            role="user",
            content="노트북 추천해주세요",
            timestamp="2024-01-01T10:00:00"
        )
        assert message.role == "user"
        assert message.content == "노트북 추천해주세요"
        assert message.timestamp == "2024-01-01T10:00:00"
        
    def test_multiturn_chat_request(self):
        """멀티턴 채팅 요청 모델 테스트"""
        request = MultiturnChatRequest(
            message="더 저렴한 걸로 추천해주세요",
            user_id="test_user_123",
            session_id="test_session_456"
        )
        assert request.message == "더 저렴한 걸로 추천해주세요"
        assert request.user_id == "test_user_123"
        assert request.session_id == "test_session_456"
        
    def test_multiturn_chat_request_new_session(self):
        """새 세션 멀티턴 채팅 요청 테스트"""
        request = MultiturnChatRequest(
            message="노트북 추천해주세요",
            user_id="test_user_123"
        )
        assert request.session_id is None
        
    def test_multiturn_chat_response(self):
        """멀티턴 채팅 응답 모델 테스트"""
        history = [
            MessageHistory(role="user", content="노트북 추천해주세요"),
            MessageHistory(role="assistant", content="추천 노트북 목록입니다.")
        ]
        
        response = MultiturnChatResponse(
            response="더 자세한 정보입니다.",
            session_id="session_123",
            thread_id="thread_123",
            message_history=history
        )
        
        assert response.response == "더 자세한 정보입니다."
        assert response.session_id == "session_123"
        assert response.thread_id == "thread_123"
        assert len(response.message_history) == 2
        assert response.message_history[0].role == "user"
        assert response.message_history[1].role == "assistant" 