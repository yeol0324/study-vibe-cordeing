from fastapi import APIRouter, HTTPException
from typing import List
from app.models.chat import ChatRequest, ChatResponse, MultiturnChatRequest, MultiturnChatResponse
from app.models.session import SessionModel
from app.agent import search_products, get_agent
from app.services.session_service import session_service

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """채팅 엔드포인트 - MCP Agent를 통한 상품 검색"""
    try:
        # MCP Agent를 통한 상품 검색
        response_text = await search_products(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 중 오류가 발생했습니다: {str(e)}")


@router.post("/multiturn", response_model=MultiturnChatResponse)
async def multiturn_chat(request: MultiturnChatRequest):
    """멀티턴 채팅 엔드포인트 - 세션 기반 대화"""
    try:
        result = session_service.process_message(
            user_id=request.user_id,
            message=request.message,
            session_id=request.session_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"대화 처리 중 오류가 발생했습니다: {str(e)}")


@router.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """세션 대화 히스토리 조회"""
    try:
        session = session_service.memory_agent.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")
            
        history = session_service.get_message_history(session.user_id)
        return {"session_id": session_id, "history": history}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"히스토리 조회 중 오류가 발생했습니다: {str(e)}")


@router.get("/users/{user_id}/sessions")
async def get_user_sessions(user_id: str):
    """사용자의 모든 세션 조회"""
    try:
        # 현재는 메모리에 저장된 세션만 조회 (실제로는 DB에서 조회해야 함)
        user_sessions = []
        for session_id, session in session_service.memory_agent.sessions.items():
            if session.user_id == user_id:
                user_sessions.append({
                    "session_id": session.session_id,
                    "thread_id": session.thread_id,
                    "created_at": session.created_at
                })
        
        return {"user_id": user_id, "sessions": user_sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"세션 조회 중 오류가 발생했습니다: {str(e)}")


@router.get("/agent/status")
async def get_agent_status():
    """MCP Agent 상태 확인"""
    try:
        agent = await get_agent()
        status = await agent.health_check()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"에이전트 상태 확인 중 오류가 발생했습니다: {str(e)}")


@router.get("/agent/tools")
async def get_agent_tools():
    """MCP Agent 사용 가능한 도구 목록"""
    try:
        agent = await get_agent()
        tools = await agent.get_available_tools()
        
        # 도구 정보 포맷팅
        tool_info = []
        for tool in tools:
            if hasattr(tool, 'name'):
                tool_info.append({
                    "name": tool.name,
                    "description": getattr(tool, 'description', 'No description available')
                })
            else:
                tool_info.append({
                    "name": str(tool),
                    "description": "Tool information not available"
                })
        
        return {"tools": tool_info, "count": len(tools)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"도구 목록 조회 중 오류가 발생했습니다: {str(e)}") 