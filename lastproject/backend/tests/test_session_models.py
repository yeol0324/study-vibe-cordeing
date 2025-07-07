"""사용자 세션 모델 테스트"""
import pytest
from datetime import datetime
from app.models.session import SessionModel, SessionRequest, SessionResponse


class TestSessionModels:
    """세션 모델 테스트 클래스"""
    
    def test_create_session_model(self):
        """세션 모델 생성 테스트"""
        session = SessionModel(
            session_id="test_session_123",
            user_id="test_user_123",
            thread_id="test_thread_123"
        )
        assert session.session_id == "test_session_123"
        assert session.user_id == "test_user_123"
        assert session.thread_id == "test_thread_123"
        assert isinstance(session.created_at, datetime)
        
    def test_session_request_validation(self):
        """세션 요청 검증 테스트"""
        request = SessionRequest(
            message="노트북 추천해주세요",
            user_id="test_user_123"
        )
        assert request.message == "노트북 추천해주세요"
        assert request.user_id == "test_user_123"
        assert request.session_id is None  # 새 세션
        
    def test_session_request_with_existing_session(self):
        """기존 세션을 사용한 요청 테스트"""
        request = SessionRequest(
            message="더 저렴한 걸로 알려주세요",
            user_id="test_user_123",
            session_id="existing_session_456"
        )
        assert request.session_id == "existing_session_456"
        
    def test_session_response_model(self):
        """세션 응답 모델 테스트"""
        response = SessionResponse(
            response="추천 노트북 목록입니다.",
            session_id="session_789",
            thread_id="thread_789"
        )
        assert response.response == "추천 노트북 목록입니다."
        assert response.session_id == "session_789"
        assert response.thread_id == "thread_789" 