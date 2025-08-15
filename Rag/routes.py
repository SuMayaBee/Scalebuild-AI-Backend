"""
RAG System API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import os
from pathlib import Path

from app.core.database import get_db
from app.core.security import get_current_user
from app.auth.db_models import User
from Rag.models import (
    DocumentUploadResponse, RAGQueryRequest, RAGQueryResponse,
    DocumentListResponse, ChatHistoryResponse, DocumentDeleteResponse,
    WebsiteProcessRequest, WebsiteProcessResponse, WebsiteScrapeResult
)
from Rag.services.rag_service import rag_service
from Rag.services.document_processor import document_processor
from Rag.services.web_scraper_service import web_scraper_service
from Rag.db_models import RAGDocument, RAGChatSession

router = APIRouter(prefix="/rag", tags=["RAG System"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document for RAG system
    
    Supported formats: PDF, DOCX, TXT, CSV, XLSX, PPTX, JSON, MD
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check if file format is supported
        if not document_processor.is_supported_format(file.filename):
            supported = ", ".join(document_processor.get_supported_formats().keys())
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format. Supported formats: {supported}"
            )
        
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file provided")
        
        # Check file size (max 50MB)
        max_size = 50 * 1024 * 1024  # 50MB
        if len(file_content) > max_size:
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 50MB")
        
        print(f"📤 Processing upload: {file.filename} ({len(file_content)} bytes)")
        
        # Extract text from document
        extraction_result = document_processor.extract_text_from_file(
            file_content=file_content,
            filename=file.filename
        )
        
        text_content = extraction_result["text"]
        file_metadata = extraction_result["metadata"]
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No text content could be extracted from the file")
        
        # Process document with RAG service
        document = await rag_service.process_document(
            user_id=current_user.id,
            file_content=text_content,
            filename=file.filename,
            file_type=Path(file.filename).suffix.lower().lstrip('.'),
            title=title or file.filename,
            metadata=file_metadata
        )
        
        return DocumentUploadResponse(
            id=document.id,
            user_id=document.user_id,
            title=document.title,
            filename=document.filename,
            file_size=document.file_size,
            file_type=document.file_type,
            chunks_count=document.chunks_count,
            status=document.status,
            created_at=document.created_at,
            updated_at=document.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@router.post("/query", response_model=RAGQueryResponse)
async def query_documents(
    request: RAGQueryRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Query documents using RAG system
    """
    try:
        # Validate user access
        if request.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Process RAG query
        result = await rag_service.query_documents(
            user_id=request.user_id,
            query=request.query,
            max_results=request.max_results or 5,
            session_id=request.session_id
        )
        
        return RAGQueryResponse(
            query=result["query"],
            answer=result["answer"],
            sources=result["sources"],
            session_id=result["session_id"],
            processing_time=result["processing_time"],
            tokens_used=result["tokens_used"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/documents", response_model=List[DocumentListResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    List user's uploaded documents
    """
    try:
        documents = db.query(RAGDocument).filter(
            RAGDocument.user_id == current_user.id
        ).offset(skip).limit(limit).all()
        
        return [
            DocumentListResponse(
                id=doc.id,
                user_id=doc.user_id,
                title=doc.title,
                filename=doc.filename,
                file_size=doc.file_size,
                file_type=doc.file_type,
                chunks_count=doc.chunks_count,
                status=doc.status,
                created_at=doc.created_at,
                updated_at=doc.updated_at
            ) for doc in documents
        ]
        
    except Exception as e:
        print(f"❌ Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.delete("/documents/{document_id}", response_model=DocumentDeleteResponse)
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Delete a document and its vectors
    """
    try:
        result = await rag_service.delete_document(
            document_id=document_id,
            user_id=current_user.id
        )
        
        if not result["success"]:
            raise HTTPException(status_code=404, detail=result["message"])
        
        return DocumentDeleteResponse(
            success=result["success"],
            message=result["message"],
            deleted_chunks=result["deleted_chunks"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@router.get("/chat/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history for a session
    """
    try:
        # Verify session belongs to user
        session = db.query(RAGChatSession).filter(
            RAGChatSession.session_id == session_id,
            RAGChatSession.user_id == current_user.id
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        history = await rag_service.get_chat_history(session_id)
        
        if not history:
            raise HTTPException(status_code=404, detail="Chat history not found")
        
        return ChatHistoryResponse(
            session_id=history["session_id"],
            user_id=history["user_id"],
            messages=[
                {
                    "role": msg["role"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"],
                    "sources": msg.get("sources", [])
                } for msg in history["messages"]
            ],
            created_at=history["created_at"],
            updated_at=history["updated_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error getting chat history: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting chat history: {str(e)}")

@router.get("/chat/sessions")
async def list_chat_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    List user's chat sessions
    """
    try:
        sessions = db.query(RAGChatSession).filter(
            RAGChatSession.user_id == current_user.id
        ).order_by(RAGChatSession.updated_at.desc()).offset(skip).limit(limit).all()
        
        return [
            {
                "session_id": session.session_id,
                "title": session.title,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
                "message_count": len(session.messages)
            } for session in sessions
        ]
        
    except Exception as e:
        print(f"❌ Error listing chat sessions: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing chat sessions: {str(e)}")

@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported file formats
    """
    return {
        "supported_formats": document_processor.get_supported_formats(),
        "max_file_size": "50MB",
        "description": "Upload documents in any of the supported formats to build your knowledge base"
    }

@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's RAG system statistics
    """
    try:
        # Count documents
        document_count = db.query(RAGDocument).filter(
            RAGDocument.user_id == current_user.id
        ).count()
        
        # Count total chunks
        from sqlalchemy import func
        total_chunks = db.query(func.sum(RAGDocument.chunks_count)).filter(
            RAGDocument.user_id == current_user.id
        ).scalar() or 0
        
        # Count chat sessions
        session_count = db.query(RAGChatSession).filter(
            RAGChatSession.user_id == current_user.id
        ).count()
        
        # Get document status breakdown
        status_counts = db.query(
            RAGDocument.status,
            func.count(RAGDocument.id)
        ).filter(
            RAGDocument.user_id == current_user.id
        ).group_by(RAGDocument.status).all()
        
        return {
            "user_id": current_user.id,
            "document_count": document_count,
            "total_chunks": total_chunks,
            "chat_sessions": session_count,
            "document_status": {status: count for status, count in status_counts},
            "supported_formats": len(document_processor.get_supported_formats())
        }
        
    except Exception as e:
        print(f"❌ Error getting user stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

@router.post("/process-website", response_model=WebsiteProcessResponse)
async def process_website(
    request: WebsiteProcessRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Process content from a website URL using LangChain WebBaseLoader
    
    Scrapes content from the provided URL and adds it to the RAG system
    """
    try:
        if not request.url.strip():
            raise HTTPException(status_code=400, detail="URL cannot be empty")
        
        print(f"🌐 Processing website: {request.url}")
        
        # Process website with RAG service using LangChain
        document = await rag_service.process_website(
            user_id=current_user.id,
            url=request.url,
            title=request.title,
            verify_ssl=request.verify_ssl,
            max_pages=request.max_pages
        )
        
        # Get scraped pages count from metadata
        scraped_pages = document.document_metadata.get("scraped_pages", 1) if document.document_metadata else 1
        
        return WebsiteProcessResponse(
            id=document.id,
            user_id=document.user_id,
            title=document.title,
            url=request.url,
            file_type=document.file_type,
            chunks_count=document.chunks_count,
            status=document.status,
            scraped_pages=scraped_pages,
            created_at=document.created_at,
            updated_at=document.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing website: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing website: {str(e)}")

@router.post("/scrape-preview")
async def scrape_preview(
    urls: List[str],
    current_user: User = Depends(get_current_user)
):
    """
    Preview content from website URLs without adding to RAG system
    
    Useful for checking what content will be extracted before uploading
    """
    try:
        if not urls:
            raise HTTPException(status_code=400, detail="No URLs provided")
        
        if len(urls) > 5:  # Limit preview to 5 URLs
            raise HTTPException(status_code=400, detail="Maximum 5 URLs allowed for preview")
        
        print(f"👀 Previewing {len(urls)} website URLs...")
        
        # Scrape URLs for preview
        scrape_results = web_scraper.scrape_multiple_urls(urls, delay=0.5)
        
        preview_results = []
        for i, result in enumerate(scrape_results):
            url = urls[i]
            
            if result["success"]:
                content_preview = result["content"][:500] + "..." if len(result["content"]) > 500 else result["content"]
                
                preview_results.append(WebsiteScrapeResult(
                    url=url,
                    success=True,
                    content_length=len(result["content"]),
                    title=result["metadata"].get("title", ""),
                    domain=result["metadata"].get("domain", ""),
                    error=None
                ))
            else:
                preview_results.append(WebsiteScrapeResult(
                    url=url,
                    success=False,
                    content_length=0,
                    title="",
                    domain="",
                    error=result.get("error", "Unknown error")
                ))
        
        return {
            "total_urls": len(urls),
            "successful_urls": sum(1 for r in preview_results if r.success),
            "results": preview_results
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error previewing websites: {e}")
        raise HTTPException(status_code=500, detail=f"Error previewing websites: {str(e)}")

@router.post("/extract-links")
async def extract_links(
    url: str,
    same_domain_only: bool = True,
    current_user: User = Depends(get_current_user)
):
    """
    Extract links from a webpage
    
    Useful for discovering related pages to scrape
    """
    try:
        if not url.strip():
            raise HTTPException(status_code=400, detail="URL cannot be empty")
        
        print(f"🔗 Extracting links from: {url}")
        
        links = web_scraper.get_page_links(url, same_domain_only=same_domain_only)
        
        return {
            "source_url": url,
            "same_domain_only": same_domain_only,
            "total_links": len(links),
            "links": links[:50]  # Limit to first 50 links
        }
        
    except Exception as e:
        print(f"❌ Error extracting links: {e}")
        raise HTTPException(status_code=500, detail=f"Error extracting links: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Check RAG system health
    """
    try:
        # Test all services
        service_status = rag_service.test_services()
        
        all_healthy = all(service_status.values())
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "services": service_status,
            "timestamp": "2025-01-15T10:00:00Z"
        }
        
    except Exception as e:
        print(f"❌ Error checking health: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2025-01-15T10:00:00Z"
        }