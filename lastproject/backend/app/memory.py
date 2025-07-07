"""멀티턴 메모리 시스템"""
import uuid
from typing import Dict, Any, List, Optional
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import InMemorySaver


class MemorySystem:
    """메모리 시스템 클래스"""
    
    def __init__(self):
        """메모리 시스템 초기화"""
        self.store = InMemoryStore()
        self.checkpointer = InMemorySaver()
    
    def get_store(self) -> InMemoryStore:
        """메모리 스토어 반환"""
        return self.store
    
    def get_checkpointer(self) -> InMemorySaver:
        """체크포인터 반환"""
        return self.checkpointer
    
    def save_user_memory(self, user_id: str, memory_data: Dict[str, Any]) -> str:
        """사용자 메모리 저장"""
        namespace = (user_id, "memories")
        memory_id = str(uuid.uuid4())
        self.store.put(namespace, memory_id, memory_data)
        return memory_id
    
    def get_user_memory(self, user_id: str, memory_id: str) -> Optional[Dict[str, Any]]:
        """특정 사용자 메모리 조회"""
        namespace = (user_id, "memories")
        memory = self.store.get(namespace, memory_id)
        return memory.value if memory else None
    
    def search_user_memories(self, user_id: str, query: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """사용자 메모리 검색"""
        namespace = (user_id, "memories")
        if query:
            memories = self.store.search(namespace, query=query, limit=limit)
        else:
            memories = self.store.search(namespace)
        return [memory.value for memory in memories]


# 전역 메모리 시스템 인스턴스
memory_system = MemorySystem() 