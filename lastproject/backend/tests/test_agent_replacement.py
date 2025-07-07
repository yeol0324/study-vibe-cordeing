import pytest
import asyncio
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# 현재 디렉토리를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.agent import get_agent
from app.mcp_agent import MCPReactAgent


class TestAgentReplacement:
    
    @pytest.mark.asyncio
    async def test_get_agent_returns_mcp_agent(self):
        """get_agent 함수가 MCP Agent를 반환하는지 테스트"""
        agent = await get_agent()
        
        assert agent is not None
        assert isinstance(agent, MCPReactAgent)
    
    @pytest.mark.asyncio
    async def test_mcp_agent_compatibility(self):
        """MCP Agent가 기존 Agent와 호환되는지 테스트"""
        agent = await get_agent()
        
        # 기본 메서드들이 존재하는지 확인
        assert hasattr(agent, 'search_and_respond')
        assert callable(getattr(agent, 'search_and_respond'))
        
        # 검색 기능 테스트
        result = await agent.search_and_respond("테스트 상품")
        assert result is not None
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_agent_health_check(self):
        """Agent 상태 확인 테스트"""
        agent = await get_agent()
        
        health_status = await agent.health_check()
        
        assert health_status is not None
        assert isinstance(health_status, dict)
        assert "llm_ready" in health_status
        assert "mcp_client_ready" in health_status
    
    @pytest.mark.asyncio
    async def test_agent_tools_integration(self):
        """Agent 도구 통합 테스트"""
        agent = await get_agent()
        
        tools = await agent.get_available_tools()
        assert tools is not None
        assert isinstance(tools, list) 