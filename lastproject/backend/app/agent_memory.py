"""메모리 기반 에이전트"""
import os
from typing import Optional, Dict, Any
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig

from app.memory import memory_system
from app.models.session import SessionModel

# env loading
from dotenv import load_dotenv
load_dotenv()


class MemoryAgent:
    """메모리 기반 에이전트 클래스"""
    
    def __init__(self):
        """메모리 에이전트 초기화"""
        self.memory_system = memory_system
        self.sessions: Dict[str, SessionModel] = {}
        
    def create_session(self, user_id: str) -> SessionModel:
        """새 세션 생성"""
        session = SessionModel.create_new_session(user_id)
        self.sessions[session.session_id] = session
        return session
        
    def get_session(self, session_id: str) -> Optional[SessionModel]:
        """세션 조회"""
        return self.sessions.get(session_id)
        
    def save_search_memory(self, user_id: str, query: str, context: str) -> str:
        """검색 메모리 저장"""
        memory_data = {
            "search_query": query,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "type": "search"
        }
        return self.memory_system.save_user_memory(user_id, memory_data)
        
    def get_user_search_history(self, user_id: str, limit: int = 5) -> list:
        """사용자 검색 기록 조회"""
        return self.memory_system.search_user_memories(user_id, limit=limit)
        
    def create_agent_graph(self):
        """메모리 기반 에이전트 그래프 생성"""
        # LLM 초기화
        print("google api key", os.getenv("GOOGLE_API_KEY"))
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-preview-05-20",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # 도구 초기화
        search_tool = DuckDuckGoSearchRun()
        tools = [search_tool]
        
        # 시스템 프롬프트 설정
        system_prompt = """
        당신은 상품 최저가 검색 전문 어시스턴트입니다.
        사용자의 과거 검색 기록과 선호도를 고려하여 개인화된 검색 결과를 제공해주세요.
        
        사용자가 요청한 상품에 대해:
        1. 과거 검색 기록을 참고하여 맞춤형 검색
        2. 상품명과 가격 정보 제공  
        3. 구매 가능한 쇼핑몰 또는 사이트 링크 제공
        
        한국어로 친절하고 상세하게 답변해주세요.
        """
        
        # React Agent 생성 (메모리 시스템 통합)
        agent = create_react_agent(
            llm,
            tools,
            checkpointer=self.memory_system.get_checkpointer(),
            store=self.memory_system.get_store(),
            prompt=system_prompt
        )
        
        return agent


# 전역 메모리 에이전트 인스턴스
memory_agent = MemoryAgent() 