import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import create_agent, search_products, get_agent


class TestAgent:
    
    @pytest.mark.asyncio
    async def test_create_agent(self):
        """Agent 생성 테스트"""
        agent = await get_agent()
        
        assert agent is not None
        assert hasattr(agent, 'llm')
        assert hasattr(agent, 'mcp_client')
    
    @pytest.mark.asyncio
    async def test_search_products(self):
        """상품 검색 기능 테스트"""
        result = await search_products("아이폰 15")
        
        assert result is not None
        assert isinstance(result, str)
        assert "아이폰 15" in result or "상품 검색" in result or "검색 결과" in result
    
    @pytest.mark.asyncio
    async def test_search_products_with_empty_query(self):
        """빈 검색어 테스트"""
        result = await search_products("")
        
        assert result is not None
        assert "검색어를 입력해주세요" in result
    
    @pytest.mark.asyncio
    async def test_search_products_with_none_query(self):
        """None 검색어 테스트"""
        result = await search_products(None)
        
        assert result is not None
        assert "검색어를 입력해주세요" in result
    
    @pytest.mark.asyncio
    async def test_agent_tool_integration(self):
        """Agent 도구 통합 테스트"""
        agent = await get_agent()
        
        # 도구 가져오기 테스트
        tools = await agent.get_available_tools()
        
        assert tools is not None
        assert isinstance(tools, list)
        
        # 검색 테스트
        result = await agent.search_and_respond("테스트 상품")
        
        assert result is not None
        assert isinstance(result, str) 