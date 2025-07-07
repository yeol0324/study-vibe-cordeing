"""메모리 시스템 테스트"""
import pytest
import uuid
from typing import Dict, Any
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver


class TestMemorySystem:
    """메모리 시스템 테스트 클래스"""
    
    def test_create_memory_store(self):
        """InMemoryStore 생성 테스트"""
        store = InMemoryStore()
        assert store is not None
        
    def test_create_memory_checkpointer(self):
        """InMemorySaver 생성 테스트"""
        checkpointer = InMemorySaver()
        assert checkpointer is not None
        
    def test_store_user_memory(self):
        """사용자 메모리 저장 테스트"""
        store = InMemoryStore()
        user_id = "test_user_123"
        namespace = (user_id, "memories")
        memory_id = str(uuid.uuid4())
        memory_data = {"search_query": "노트북", "timestamp": "2024-01-01"}
        
        # 메모리 저장
        store.put(namespace, memory_id, memory_data)
        
        # 저장된 메모리 조회
        retrieved_memory = store.get(namespace, memory_id)
        assert retrieved_memory is not None
        assert retrieved_memory.value == memory_data
        
    def test_search_user_memories(self):
        """사용자 메모리 검색 테스트"""
        store = InMemoryStore()
        user_id = "test_user_123"
        namespace = (user_id, "memories")
        
        # 테스트 메모리 데이터 저장
        test_memories = [
            {"search_query": "노트북", "category": "전자제품"},
            {"search_query": "마우스", "category": "전자제품"},
            {"search_query": "책", "category": "도서"}
        ]
        
        for i, memory in enumerate(test_memories):
            store.put(namespace, f"memory_{i}", memory)
        
        # 메모리 검색
        memories = store.search(namespace)
        assert len(memories) == 3
        
    def test_session_isolation(self):
        """세션 격리 테스트"""
        store = InMemoryStore()
        
        # 다른 사용자의 메모리 저장
        user1_namespace = ("user1", "memories")
        user2_namespace = ("user2", "memories")
        
        store.put(user1_namespace, "mem1", {"data": "user1 data"})
        store.put(user2_namespace, "mem1", {"data": "user2 data"})
        
        # 각 사용자의 메모리가 분리되어 있는지 확인
        user1_memories = store.search(user1_namespace)
        user2_memories = store.search(user2_namespace)
        
        assert len(user1_memories) == 1
        assert len(user2_memories) == 1
        assert user1_memories[0].value["data"] == "user1 data"
        assert user2_memories[0].value["data"] == "user2 data" 