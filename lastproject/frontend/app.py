import streamlit as st
import requests
import time
import os
import uuid

# 페이지 설정
st.set_page_config(
    page_title="상품 검색 챗봇 (MCP Agent)",
    page_icon="🤖",
    layout="wide"
)

# 상수 설정
BACKEND_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 5 if os.getenv("STREAMLIT_TESTING") else 30  # 테스트 환경에서는 짧은 타임아웃

def call_mcp_chat_api(message: str) -> dict:
    """MCP Agent 채팅 API 호출 함수"""
    try:
        with st.spinner("MCP Agent가 상품을 검색 중입니다..."):
            payload = {"message": message}
                
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "response": f"서버 오류가 발생했습니다. (상태 코드: {response.status_code})"
                }
                
    except requests.exceptions.ConnectionError:
        return {
            "response": "백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요."
        }
    except requests.exceptions.Timeout:
        return {
            "response": "요청 시간이 초과되었습니다. 다시 시도해주세요."
        }
    except requests.exceptions.RequestException as e:
        return {
            "response": f"요청 중 오류가 발생했습니다: {str(e)}"
        }
    except Exception as e:
        return {
            "response": f"예상치 못한 오류가 발생했습니다: {str(e)}"
        }

def call_multiturn_api(message: str, user_id: str, session_id: str = None) -> dict:
    """멀티턴 채팅 API 호출 함수 (기존 기능 유지)"""
    try:
        with st.spinner("AI가 상품을 검색 중입니다..."):
            payload = {
                "message": message,
                "user_id": user_id
            }
            
            # 기존 세션이 있으면 session_id 추가
            if session_id:
                payload["session_id"] = session_id
                
            response = requests.post(
                f"{BACKEND_URL}/chat/multiturn",
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "response": f"서버 오류가 발생했습니다. (상태 코드: {response.status_code})",
                    "session_id": None,
                    "thread_id": None,
                    "message_history": []
                }
                
    except requests.exceptions.ConnectionError:
        return {
            "response": "백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.",
            "session_id": None,
            "thread_id": None,
            "message_history": []
        }
    except requests.exceptions.Timeout:
        return {
            "response": "요청 시간이 초과되었습니다. 다시 시도해주세요.",
            "session_id": None,
            "thread_id": None,
            "message_history": []
        }
    except requests.exceptions.RequestException as e:
        return {
            "response": f"요청 중 오류가 발생했습니다: {str(e)}",
            "session_id": None,
            "thread_id": None,
            "message_history": []
        }
    except Exception as e:
        return {
            "response": f"예상치 못한 오류가 발생했습니다: {str(e)}",
            "session_id": None,
            "thread_id": None,
            "message_history": []
        }

def get_agent_status() -> dict:
    """MCP Agent 상태 조회"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/chat/agent/status",
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"상태 조회 실패: {response.status_code}"}
            
    except Exception as e:
        return {"error": f"요청 실패: {str(e)}"}

def get_agent_tools() -> dict:
    """MCP Agent 도구 목록 조회"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/chat/agent/tools",
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"tools": [], "error": f"도구 조회 실패: {response.status_code}"}
            
    except Exception as e:
        return {"tools": [], "error": f"요청 실패: {str(e)}"}

def get_session_history(session_id: str) -> dict:
    """세션 히스토리 조회"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/chat/sessions/{session_id}/history",
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"history": []}
            
    except Exception:
        return {"history": []}

def display_response_with_stream(response: str):
    """응답을 스트리밍 방식으로 표시"""
    # 테스트 환경에서는 스트리밍 효과 생략
    if os.getenv("STREAMLIT_TESTING"):
        st.markdown(response)
        return response
    
    placeholder = st.empty()
    displayed_text = ""
    
    for char in response:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(0.02)  # 타이핑 효과
    
    return response

# 메인 앱 UI
st.title("🤖 상품 검색 챗봇 (MCP Agent)")
st.markdown("새로운 MCP Agent를 사용한 상품 검색 챗봇입니다. 네이버 검색과 Exa 검색을 활용한 최신 웹 검색 기능을 제공합니다.")

# 탭 생성
tab1, tab2, tab3 = st.tabs(["💬 MCP Agent 채팅", "📜 멀티턴 채팅", "🔧 Agent 정보"])

with tab1:
    st.header("🆕 MCP Agent 채팅")
    st.markdown("**새로운 MCP Agent**를 사용한 채팅입니다. 향상된 웹 검색 기능을 제공합니다.")
    
    # MCP 세션 상태 초기화
    if "mcp_messages" not in st.session_state:
        st.session_state.mcp_messages = []

    # MCP 채팅 히스토리 표시
    for message in st.session_state.mcp_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # MCP 사용자 입력 처리
    if mcp_prompt := st.chat_input("MCP Agent에게 상품에 대해 질문해주세요!", key="mcp_input"):
        # 빈 메시지 체크
        if not mcp_prompt.strip():
            st.warning("메시지를 입력해주세요.")
        else:
            # 사용자 메시지 추가 및 표시
            st.session_state.mcp_messages.append({"role": "user", "content": mcp_prompt})
            with st.chat_message("user"):
                st.markdown(mcp_prompt)

            # MCP API 호출
            with st.chat_message("assistant"):
                result = call_mcp_chat_api(mcp_prompt)
                
                # 응답 표시
                response = result.get("response", "응답을 받을 수 없습니다.")
                final_response = display_response_with_stream(response)
                
            # 어시스턴트 응답을 세션 상태에 저장
            st.session_state.mcp_messages.append({"role": "assistant", "content": final_response})

with tab2:
    st.header("📜 멀티턴 채팅 (기존)")
    st.markdown("**기존 멀티턴 메모리 기능**을 사용한 채팅입니다. 대화 히스토리를 기억합니다.")
    
    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

    if "session_id" not in st.session_state:
        st.session_state.session_id = None

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None

    # 채팅 히스토리 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("상품에 대해 질문해주세요!", key="multiturn_input"):
        # 빈 메시지 체크
        if not prompt.strip():
            st.warning("메시지를 입력해주세요.")
        else:
            # 사용자 메시지 추가 및 표시
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # 멀티턴 API 호출
            with st.chat_message("assistant"):
                result = call_multiturn_api(
                    message=prompt,
                    user_id=st.session_state.user_id,
                    session_id=st.session_state.session_id
                )
                
                # 세션 정보 업데이트
                if result.get("session_id"):
                    st.session_state.session_id = result["session_id"]
                if result.get("thread_id"):
                    st.session_state.thread_id = result["thread_id"]
                
                # 응답 표시
                response = result.get("response", "응답을 받을 수 없습니다.")
                final_response = display_response_with_stream(response)
                
            # 어시스턴트 응답을 세션 상태에 저장
            st.session_state.messages.append({"role": "assistant", "content": final_response})

with tab3:
    st.header("🔧 MCP Agent 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Agent 상태 확인", use_container_width=True):
            status = get_agent_status()
            
            if "error" in status:
                st.error(f"❌ 상태 확인 실패: {status['error']}")
            else:
                st.success("✅ Agent 상태 정보")
                st.json(status)
    
    with col2:
        if st.button("🛠️ 사용 가능한 도구 확인", use_container_width=True):
            tools_info = get_agent_tools()
            
            if "error" in tools_info:
                st.error(f"❌ 도구 확인 실패: {tools_info['error']}")
            else:
                st.success(f"✅ 사용 가능한 도구 ({tools_info.get('count', 0)}개)")
                
                if tools_info.get('tools'):
                    for i, tool in enumerate(tools_info['tools'], 1):
                        st.markdown(f"**{i}. {tool.get('name', 'Unknown Tool')}**")
                        st.markdown(f"   - {tool.get('description', 'No description')}")
                else:
                    st.info("현재 사용 가능한 도구가 없습니다.")

# 사이드바에 정보
with st.sidebar:
    st.header("💡 사용법")
    
    st.subheader("🆕 MCP Agent")
    st.markdown("""
    **새로운 기능!** Model Context Protocol을 사용한 향상된 검색
    - 네이버 검색 연동
    - Exa AI 검색 연동  
    - 더 정확한 상품 정보 제공
    """)
    
    st.subheader("📜 멀티턴 채팅")
    st.markdown("""
    **기존 기능** 대화 히스토리를 기억하는 채팅
    - 이전 대화 참조 가능
    - 개인화된 추천 제공
    """)
    
    st.markdown("---")
    st.markdown("""
    **예시 질문:**
    - "iPhone 15 Pro 가격 알려줘"
    - "노트북 추천해줘"
    - "무선 이어폰 비교해줘"
    """)
    
    # MCP 세션 정보
    st.header("🔍 MCP Agent")
    mcp_msg_count = len(st.session_state.get("mcp_messages", []))
    st.metric("대화 수", mcp_msg_count)
    
    # 멀티턴 세션 정보 표시
    st.header("📜 멀티턴 세션 정보")
    if st.session_state.get("session_id"):
        st.text(f"세션 ID: {st.session_state.session_id[:8]}...")
        st.text(f"스레드 ID: {st.session_state.thread_id[:8] if st.session_state.thread_id else 'None'}...")
    else:
        st.text("새 세션 (첫 메시지 후 생성)")
    
    # 세션 히스토리 조회
    if st.session_state.get("session_id") and st.button("📜 전체 히스토리 조회"):
        history_data = get_session_history(st.session_state.session_id)
        if history_data.get("history"):
            st.subheader("대화 히스토리")
            for msg in history_data["history"]:
                role_icon = "👤" if msg["role"] == "user" else "🤖"
                st.text(f"{role_icon} {msg['content'][:50]}...")
        else:
            st.text("히스토리가 없습니다.")
    
    # 채팅 기록 삭제 버튼들
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ MCP 채팅 삭제", use_container_width=True):
            st.session_state.mcp_messages = []
            st.rerun()
    
    with col2:
        if st.button("🗑️ 멀티턴 채팅 삭제", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.session_state.thread_id = None
            st.rerun() 