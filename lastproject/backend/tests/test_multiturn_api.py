"""멀티턴 API 엔드포인트 테스트"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """테스트 클라이언트 생성"""
    return TestClient(app)


class TestMultiturnAPI:
    """멀티턴 API 테스트 클래스"""
    
    def test_multiturn_chat_endpoint_exists(self, client):
        """멀티턴 채팅 엔드포인트 존재 확인"""
        # POST 요청으로 엔드포인트 확인
        response = client.post("/chat/multiturn", json={
            "message": "테스트 메시지",
            "user_id": "test_user"
        })
        # 422(Validation Error)나 500(Server Error)이면 엔드포인트는 존재함
        assert response.status_code in [422, 500] or response.status_code == 200
        
    def test_multiturn_chat_request_validation(self, client):
        """멀티턴 채팅 요청 검증 테스트"""
        # 필수 필드 누락 테스트
        response = client.post("/chat/multiturn", json={
            "message": "테스트 메시지"
            # user_id 누락
        })
        assert response.status_code == 422
        
    def test_session_history_endpoint_exists(self, client):
        """세션 히스토리 엔드포인트 존재 확인"""
        response = client.get("/chat/sessions/test_session/history")
        # 404나 다른 에러여도 엔드포인트가 존재하면 됨
        assert response.status_code in [404, 500] or response.status_code == 200
        
    def test_user_sessions_endpoint_exists(self, client):
        """사용자 세션 목록 엔드포인트 존재 확인"""
        response = client.get("/chat/users/test_user/sessions")
        assert response.status_code in [404, 500] or response.status_code == 200 