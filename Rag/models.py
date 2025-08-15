"""
Pydantic models for RAG system
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentUploadRequest(BaseModel):
    user_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []

class DocumentUploadResponse(BaseModel):
    id: int
    user_id: int
    title: str
    filename: str
    file_size: int
    file_type: str
    chunks_count: int
    status: str
    created_at: datetime
    updated_at: datetime

class RAGQueryRequest(BaseModel):
    user_id: int
    query: str
    session_id: Optional[str] = None
    max_results: Optional[int] = 5
    include_sources: Optional[bool] = True

class DocumentChunk(BaseModel):
    content: str
    metadata: Dict[str, Any]
    score: float

class RAGQueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[DocumentChunk]
    session_id: str
    processing_time: float
    tokens_used: int

class DocumentListResponse(BaseModel):
    id: int
    user_id: int
    title: str
    filename: str
    file_size: int
    file_type: str
    chunks_count: int
    status: str
    created_at: datetime
    updated_at: datetime

class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    sources: Optional[List[DocumentChunk]] = []

class ChatHistoryResponse(BaseModel):
    session_id: str
    user_id: int
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime

class DocumentDeleteResponse(BaseModel):
    success: bool
    message: str
    deleted_chunks: int

class WebsiteProcessRequest(BaseModel):
    url: str
    title: Optional[str] = None
    verify_ssl: Optional[bool] = True
    max_pages: Optional[int] = 1

class WebsiteProcessResponse(BaseModel):
    id: int
    user_id: int
    title: str
    url: str
    file_type: str
    chunks_count: int
    status: str
    scraped_pages: int
    created_at: datetime
    updated_at: datetime

class WebsiteScrapeResult(BaseModel):
    url: str
    success: bool
    content_length: int
    title: str
    domain: str
    error: Optional[str] = None