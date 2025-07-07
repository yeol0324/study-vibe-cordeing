"""메모리 기반 에이전트 테스트"""
import pytest
from unittest.mock import Mock, patch
from app.agent_memory import MemoryAgent
from app.models.session import SessionModel


class TestMemoryAgent:
    """메모리 에이전트 테스트 클래스"""
    
    def test_create_memory_agent(self):
        """메모리 에이전트 생성 테스트"""
        agent = MemoryAgent()
        assert agent is not None
        assert agent.memory_system is not None
        
    def test_create_session(self):
        """세션 생성 테스트"""
        agent = MemoryAgent()
        user_id = "test_user_123"
        
        session = agent.create_session(user_id)
        assert isinstance(session, SessionModel)
        assert session.user_id == user_id
        assert session.session_id is not None
        assert session.thread_id is not None
        
    def test_get_session(self):
        """세션 조회 테스트"""
        agent = MemoryAgent()
        user_id = "test_user_123"
        
        # 세션 생성
        created_session = agent.create_session(user_id)
        
        # 세션 조회
        retrieved_session = agent.get_session(created_session.session_id)
        assert retrieved_session is not None
        assert retrieved_session.session_id == created_session.session_id
        assert retrieved_session.user_id == user_id
        
    def test_get_nonexistent_session(self):
        """존재하지 않는 세션 조회 테스트"""
        agent = MemoryAgent()
        session = agent.get_session("nonexistent_session")
        assert session is None
        
    @patch('app.agent_memory.create_react_agent')
    def test_create_agent_graph(self, mock_create_agent):
        """에이전트 그래프 생성 테스트"""
        # Mock 설정
        mock_graph = Mock()
        mock_create_agent.return_value = mock_graph
        
        agent = MemoryAgent()
        graph = agent.create_agent_graph()
        
        assert graph is not None
        mock_create_agent.assert_called_once()
        
    def test_save_search_memory(self):
        """검색 메모리 저장 테스트"""
        agent = MemoryAgent()
        user_id = "test_user_123"
        
        # 메모리 저장
        memory_id = agent.save_search_memory(user_id, "노트북", "전자제품 검색")
        assert memory_id is not None
        
        # 저장된 메모리 조회
        search_history = agent.get_user_search_history(user_id)
        assert len(search_history) == 1
        assert search_history[0]["search_query"] == "노트북"
        assert search_history[0]["context"] == "전자제품 검색"
        assert search_history[0]["type"] == "search" 