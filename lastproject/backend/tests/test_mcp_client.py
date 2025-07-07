import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mcp_client import MCPWebSearchClient


class TestMCPWebSearchClient:
    
    @pytest.fixture
    def mcp_client(self):
        """MCP 클라이언트 인스턴스 생성"""
        return MCPWebSearchClient()
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, mcp_client):
        """MCP 클라이언트 초기화 테스트"""
        assert mcp_client is not None
        assert hasattr(mcp_client, 'client')
    
    @pytest.mark.asyncio
    async def test_get_tools(self, mcp_client):
        """MCP 도구 가져오기 테스트"""
        # Mock MCP client
        mcp_client.client = AsyncMock()
        mcp_client.client.get_tools.return_value = [
            MagicMock(name="web_search"),
            MagicMock(name="exa_search")
        ]
        
        tools = await mcp_client.get_tools()
        
        assert tools is not None
        assert len(tools) >= 0
        mcp_client.client.get_tools.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_search_web(self, mcp_client):
        """웹 검색 기능 테스트"""
        # Mock 검색 결과
        mock_results = [
            {
                "title": "테스트 제품",
                "url": "https://example.com/product",
                "snippet": "테스트 제품 설명"
            }
        ]
        
        # Mock MCP client
        mcp_client.client = AsyncMock()
        
        results = await mcp_client.search_web("테스트 검색어")
        
        assert results is not None
        assert isinstance(results, list) 