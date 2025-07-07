import os
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

from .mcp_client import MCPWebSearchClient

load_dotenv()


class MCPReactAgent:
    """MCP 기반 React Agent"""
    
    def __init__(self):
        """MCP React Agent 초기화"""
        # Google Gemini LLM 초기화
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        # MCP 클라이언트 초기화
        self.mcp_client = MCPWebSearchClient()
        
        # 에이전트 (나중에 초기화)
        self.agent = None
    
    async def create_agent(self):
        """MCP 도구를 사용하는 React Agent 생성"""
        try:
            # MCP 도구 가져오기
            tools = await self.mcp_client.get_tools()
            
            # React Agent 생성
            if tools:
                self.agent = create_react_agent(self.llm, tools)
            else:
                # 도구가 없으면 기본 에이전트 생성 (더미 도구 포함)
                dummy_tools = []  # 빈 도구 리스트
                self.agent = create_react_agent(self.llm, dummy_tools)
                
            return self.agent
            
        except Exception as e:
            print(f"에이전트 생성 실패: {e}")
            # 기본 에이전트 생성
            self.agent = create_react_agent(self.llm, [])
            return self.agent
    
    async def search_and_respond(self, query: str) -> str:
        """웹 검색을 수행하고 응답 생성"""
        try:
            # 에이전트가 없으면 생성
            if not self.agent:
                await self.create_agent()
            
            # 에이전트 실행
            result = await self.agent.ainvoke({
                "messages": [("user", query)]
            })
            
            # 응답 추출
            if result and "messages" in result:
                messages = result["messages"]
                if messages:
                    # 마지막 메시지 내용 반환
                    last_message = messages[-1]
                    if hasattr(last_message, 'content'):
                        return last_message.content
                    elif isinstance(last_message, dict) and 'content' in last_message:
                        return last_message['content']
            
            # 기본 응답 (에이전트 응답이 없는 경우)
            return f"'{query}'에 대한 검색을 수행했지만 적절한 응답을 생성하지 못했습니다."
            
        except Exception as e:
            print(f"검색 및 응답 생성 실패: {e}")
            
            # 대체 검색 (MCP 클라이언트 직접 사용)
            try:
                search_results = await self.mcp_client.search_web(query)
                if search_results:
                    response = f"'{query}'에 대한 검색 결과:\n\n"
                    for i, result in enumerate(search_results[:3], 1):
                        title = result.get('title', '제목 없음')
                        snippet = result.get('snippet', '설명 없음')
                        url = result.get('url', '')
                        response += f"{i}. {title}\n{snippet}\n{url}\n\n"
                    return response
                else:
                    return f"'{query}'에 대한 검색 결과를 찾을 수 없습니다."
            except Exception as fallback_error:
                print(f"대체 검색도 실패: {fallback_error}")
                return f"'{query}'에 대한 검색 중 오류가 발생했습니다."
    
    async def get_available_tools(self) -> List[Any]:
        """사용 가능한 MCP 도구 목록 반환"""
        return await self.mcp_client.get_tools()
    
    async def health_check(self) -> Dict[str, Any]:
        """에이전트 상태 확인"""
        status = {
            "llm_ready": self.llm is not None,
            "mcp_client_ready": self.mcp_client is not None,
            "agent_ready": self.agent is not None,
            "tools_count": 0
        }
        
        try:
            tools = await self.get_available_tools()
            status["tools_count"] = len(tools) if tools else 0
        except Exception as e:
            status["tools_error"] = str(e)
        
        return status 