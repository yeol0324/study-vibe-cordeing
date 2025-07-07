import asyncio
import os
from typing import List, Dict, Any
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

load_dotenv()


class MCPWebSearchClient:
    """MCP 웹 검색 클라이언트"""
    
    def __init__(self):
        """MCP 클라이언트 초기화"""
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """MCP 멀티서버 클라이언트 초기화"""
        # 환경 변수에서 MCP URL 가져오기
        naver_url = os.getenv("NAVER_SEARCH_MCP_URL")
        exa_url = os.getenv("EXA_SEARCH_MCP_URL")
        
        server_config = {}
        
        # 네이버 검색 MCP 서버 설정
        if naver_url:
            server_config["naver_search"] = {
                "url": naver_url,
                "transport": "streamable_http"
            }
        
        # Exa 검색 MCP 서버 설정
        if exa_url:
            server_config["exa_search"] = {
                "url": exa_url,
                "transport": "streamable_http"
            }
        
        # MCP 클라이언트 생성
        if server_config:
            self.client = MultiServerMCPClient(server_config)
        else:
            # 기본 더미 클라이언트 (테스트용)
            self.client = None
    
    async def get_tools(self) -> List[Any]:
        """MCP 서버에서 사용 가능한 도구 가져오기"""
        if not self.client:
            return []
        
        try:
            tools = await self.client.get_tools()
            return tools if tools else []
        except Exception as e:
            print(f"MCP 도구 가져오기 실패: {e}")
            return []
    
    async def search_web(self, query: str) -> List[Dict[str, Any]]:
        """웹 검색 수행"""
        if not self.client:
            # 더미 검색 결과 반환 (개발용)
            return [
                {
                    "title": f"검색 결과: {query}",
                    "url": "https://example.com",
                    "snippet": f"{query}에 대한 검색 결과입니다."
                }
            ]
        
        try:
            tools = await self.get_tools()
            # 웹 검색 도구 찾기
            search_tool = None
            for tool in tools:
                if hasattr(tool, 'name') and 'search' in tool.name.lower():
                    search_tool = tool
                    break
            
            if search_tool:
                # 도구 실행
                result = await search_tool.arun(query)
                return result if isinstance(result, list) else [result]
            else:
                return []
                
        except Exception as e:
            print(f"웹 검색 실패: {e}")
            return [] 