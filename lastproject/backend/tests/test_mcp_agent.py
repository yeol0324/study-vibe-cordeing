import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mcp_agent import MCPReactAgent


class TestMCPReactAgent:
    
    @pytest.fixture
    def mcp_agent(self):
        """MCP React Agent 인스턴스 생성"""
        return MCPReactAgent()
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, mcp_agent):
        """MCP React Agent 초기화 테스트"""
        assert mcp_agent is not None
        assert hasattr(mcp_agent, 'llm')
        assert hasattr(mcp_agent, 'mcp_client')
        assert hasattr(mcp_agent, 'agent')
    
    @pytest.mark.asyncio
    async def test_create_agent(self, mcp_agent):
        """에이전트 생성 테스트"""
        # Mock MCP tools
        mock_tools = [MagicMock(name="web_search"), MagicMock(name="exa_search")]
        
        with patch.object(mcp_agent.mcp_client, 'get_tools', return_value=mock_tools):
            agent = await mcp_agent.create_agent()
            
            assert agent is not None
    
    @pytest.mark.asyncio 
    async def test_search_and_respond(self, mcp_agent):
        """검색 및 응답 생성 테스트"""
        # Mock 검색 결과
        mock_search_results = [
            {
                "title": "테스트 상품",
                "url": "https://example.com/product",
                "snippet": "테스트 상품 설명"
            }
        ]
        
        # Mock agent
        mock_agent = AsyncMock()
        mock_agent.ainvoke.return_value = {
            "messages": [
                MagicMock(content="테스트 상품에 대한 검색 결과입니다.")
            ]
        }
        
        mcp_agent.agent = mock_agent
        
        result = await mcp_agent.search_and_respond("테스트 상품 검색")
        
        assert result is not None
        assert isinstance(result, str)
        mock_agent.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_available_tools(self, mcp_agent):
        """사용 가능한 도구 목록 테스트"""
        # Mock tools
        mock_tools = [
            MagicMock(name="web_search"),
            MagicMock(name="exa_search")
        ]
        
        with patch.object(mcp_agent.mcp_client, 'get_tools', return_value=mock_tools):
            tools = await mcp_agent.get_available_tools()
            
            assert tools is not None
            assert len(tools) == 2 