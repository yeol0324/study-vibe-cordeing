from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel
from fastapi import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "온라인 쇼핑 최저가 검색 챗봇 API"}

@app.get("/health")
def health():
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

class SearchRequest(BaseModel):
    query: str
    session_id: str

class SearchResponse(BaseModel):
    task_id: str
    status: str
    message: str

@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest = Body(...)):
    # 실제 검색 로직은 추후 구현
    return SearchResponse(
        task_id="task_dummy",
        status="processing",
        message="검색을 시작합니다."
    ) 