import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "온라인 쇼핑 최저가 검색 챗봇 API"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data 

def test_search():
    payload = {"query": "아이폰 15 케이스", "session_id": "user_123"}
    response = client.post("/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "task_dummy"
    assert data["status"] == "processing"
    assert data["message"] == "검색을 시작합니다." 