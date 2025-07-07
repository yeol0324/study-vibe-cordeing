import os
from typing import Optional
from .mcp_agent import MCPReactAgent


# 전역 MCP Agent 인스턴스 (싱글톤 패턴)
_mcp_agent_instance = None


async def get_agent() -> MCPReactAgent:
    """MCP React Agent 인스턴스를 반환합니다 (싱글톤)"""
    global _mcp_agent_instance
    
    if _mcp_agent_instance is None:
        _mcp_agent_instance = MCPReactAgent()
        # 에이전트 초기화
        await _mcp_agent_instance.create_agent()
    
    return _mcp_agent_instance


async def search_products(query: Optional[str]) -> str:
    """상품 검색 함수 (MCP Agent 사용)"""
    if not query or query.strip() == "":
        return "검색어를 입력해주세요."
    
    try:
        # MCP Agent 가져오기
        agent = await get_agent()
        
        # 검색 및 응답 생성
        result = await agent.search_and_respond(query)
        return result
        
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}"


# 기존 함수와의 호환성을 위한 동기 래퍼 함수
def create_agent():
    """기존 호환성을 위한 함수 (deprecated)"""
    import asyncio
    
    try:
        # 이벤트 루프가 있으면 사용, 없으면 새로 생성
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 이미 실행 중인 루프에서는 새 태스크 생성
            task = asyncio.create_task(get_agent())
            return task
        else:
            return asyncio.run(get_agent())
    except RuntimeError:
        # 새 이벤트 루프 생성
        return asyncio.run(get_agent()) 