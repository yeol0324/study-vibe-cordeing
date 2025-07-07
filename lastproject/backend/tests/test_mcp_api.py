import pytest
import asyncio
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app


class TestMCPAPI:
    
    @pytest.fixture
    def client(self):
        """FastAPI 테스트 클라이언트"""
        return TestClient(app)
    
    def test_chat_endpoint_basic(self, client):
        """기본 채팅 엔드포인트 테스트"""
        response = client.post(
            "/chat",
            json={"message": "아이폰 15 최저가 검색"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert isinstance(data["response"], str)
    
    def test_chat_endpoint_empty_message(self, client):
        """빈 메시지 테스트"""
        response = client.post(
            "/chat",
            json={"message": ""}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "검색어를 입력해주세요" in data["response"]
    
    def test_health_check_endpoint(self, client):
        """상태 확인 엔드포인트 테스트"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_agent_status_endpoint(self, client):
        """에이전트 상태 확인 엔드포인트 테스트"""
        response = client.get("/chat/agent/status")
        
        assert response.status_code == 200
        data = response.json()
        assert "llm_ready" in data
        assert "mcp_client_ready" in data
        assert "agent_ready" in data
    
    def test_agent_tools_endpoint(self, client):
        """에이전트 도구 목록 엔드포인트 테스트"""
        response = client.get("/chat/agent/tools")
        
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert isinstance(data["tools"], list) 