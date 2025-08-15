# RAG System API Examples

## Authentication
All endpoints require authentication. Include your JWT token in the Authorization header:
```
Authorization: Bearer your_jwt_token_here
```

## 1. Upload Document

**Endpoint:** `POST /rag/upload`  
**Content-Type:** `multipart/form-data`

### cURL Example:
```bash
curl -X POST "http://localhost:8000/rag/upload" \
  -H "Authorization: Bearer your_jwt_token" \
  -F "file=@/path/to/your/document.pdf" \
  -F "title=My Important Document" \
  -F "description=This document contains important information"
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/upload"
headers = {"Authorization": "Bearer your_jwt_token"}

# Upload a file
files = {"file": open("document.pdf", "rb")}
data = {
    "title": "My Document Title",
    "description": "Optional description"
}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

### Response:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "My Important Document",
  "filename": "document.pdf",
  "file_size": 1024000,
  "file_type": "pdf",
  "chunks_count": 15,
  "status": "completed",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:01:00Z"
}
```

## 2. Query Documents (Ask Questions)

**Endpoint:** `POST /rag/query`  
**Content-Type:** `application/json`

### Request Body:
```json
{
  "user_id": 123,
  "query": "What are the main features of the RAG system?",
  "session_id": "optional-session-uuid",
  "max_results": 5,
  "include_sources": true
}
```

### cURL Example:
```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 123,
    "query": "What is Python and who created it?",
    "max_results": 5
  }'
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/query"
headers = {
    "Authorization": "Bearer your_jwt_token",
    "Content-Type": "application/json"
}

data = {
    "user_id": 123,
    "query": "What are the key benefits of using this system?",
    "session_id": "chat-session-123",
    "max_results": 5,
    "include_sources": True
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['sources'])}")
```

### Response:
```json
{
  "query": "What are the main features of the RAG system?",
  "answer": "The RAG system has several key features: 1) Document upload and processing for multiple file formats, 2) Text chunking and embedding generation, 3) Vector storage in Pinecone for semantic search, 4) GPT-powered answer generation based on document context, and 5) Persistent chat sessions with source citations.",
  "sources": [
    {
      "content": "The RAG system combines document processing with AI...",
      "metadata": {
        "document_id": 1,
        "filename": "rag_guide.pdf",
        "title": "RAG System Guide",
        "chunk_index": 2,
        "score": 0.95
      },
      "score": 0.95
    }
  ],
  "session_id": "chat-session-123",
  "processing_time": 2.34,
  "tokens_used": 450
}
```

## 3. List User Documents

**Endpoint:** `GET /rag/documents`

### cURL Example:
```bash
curl -X GET "http://localhost:8000/rag/documents?skip=0&limit=10" \
  -H "Authorization: Bearer your_jwt_token"
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/documents"
headers = {"Authorization": "Bearer your_jwt_token"}
params = {"skip": 0, "limit": 10}

response = requests.get(url, headers=headers, params=params)
documents = response.json()

for doc in documents:
    print(f"Document: {doc['title']} ({doc['file_type']}) - {doc['chunks_count']} chunks")
```

### Response:
```json
[
  {
    "id": 1,
    "user_id": 123,
    "title": "Python Guide",
    "filename": "python_guide.pdf",
    "file_size": 1024000,
    "file_type": "pdf",
    "chunks_count": 15,
    "status": "completed",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:01:00Z"
  }
]
```

## 4. Delete Document

**Endpoint:** `DELETE /rag/documents/{document_id}`

### cURL Example:
```bash
curl -X DELETE "http://localhost:8000/rag/documents/1" \
  -H "Authorization: Bearer your_jwt_token"
```

### Python Example:
```python
import requests

document_id = 1
url = f"http://localhost:8000/rag/documents/{document_id}"
headers = {"Authorization": "Bearer your_jwt_token"}

response = requests.delete(url, headers=headers)
result = response.json()

print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
```

### Response:
```json
{
  "success": true,
  "message": "Document 'Python Guide' deleted successfully",
  "deleted_chunks": 15
}
```

## 5. Get Chat History

**Endpoint:** `GET /rag/chat/{session_id}`

### cURL Example:
```bash
curl -X GET "http://localhost:8000/rag/chat/chat-session-123" \
  -H "Authorization: Bearer your_jwt_token"
```

### Python Example:
```python
import requests

session_id = "chat-session-123"
url = f"http://localhost:8000/rag/chat/{session_id}"
headers = {"Authorization": "Bearer your_jwt_token"}

response = requests.get(url, headers=headers)
history = response.json()

print(f"Session: {history['session_id']}")
for message in history['messages']:
    print(f"{message['role']}: {message['content'][:100]}...")
```

### Response:
```json
{
  "session_id": "chat-session-123",
  "user_id": 123,
  "messages": [
    {
      "role": "user",
      "content": "What is Python?",
      "timestamp": "2025-01-15T10:00:00Z",
      "sources": []
    },
    {
      "role": "assistant",
      "content": "Python is a high-level programming language...",
      "timestamp": "2025-01-15T10:00:05Z",
      "sources": [
        {
          "content": "Python is a programming language...",
          "metadata": {"document_id": 1, "score": 0.95}
        }
      ]
    }
  ],
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:00:05Z"
}
```

## 6. List Chat Sessions

**Endpoint:** `GET /rag/chat/sessions`

### cURL Example:
```bash
curl -X GET "http://localhost:8000/rag/chat/sessions?skip=0&limit=10" \
  -H "Authorization: Bearer your_jwt_token"
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/chat/sessions"
headers = {"Authorization": "Bearer your_jwt_token"}
params = {"skip": 0, "limit": 10}

response = requests.get(url, headers=headers, params=params)
sessions = response.json()

for session in sessions:
    print(f"Session: {session['title']} ({session['message_count']} messages)")
```

### Response:
```json
[
  {
    "session_id": "chat-session-123",
    "title": "What is Python?",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:05:00Z",
    "message_count": 4
  }
]
```

## 7. Get Supported Formats

**Endpoint:** `GET /rag/supported-formats`

### cURL Example:
```bash
curl -X GET "http://localhost:8000/rag/supported-formats"
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/supported-formats"
response = requests.get(url)
formats = response.json()

print("Supported formats:")
for ext, desc in formats['supported_formats'].items():
    print(f"  {ext}: {desc}")
```

### Response:
```json
{
  "supported_formats": {
    "pdf": "PDF Document",
    "txt": "Text File",
    "docx": "Word Document",
    "xlsx": "Excel Spreadsheet",
    "csv": "CSV File",
    "pptx": "PowerPoint Presentation",
    "json": "JSON File",
    "md": "Markdown File"
  },
  "max_file_size": "50MB",
  "description": "Upload documents in any of the supported formats to build your knowledge base"
}
```

## 8. Get User Statistics

**Endpoint:** `GET /rag/stats`

### cURL Example:
```bash
curl -X GET "http://localhost:8000/rag/stats" \
  -H "Authorization: Bearer your_jwt_token"
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/stats"
headers = {"Authorization": "Bearer your_jwt_token"}

response = requests.get(url, headers=headers)
stats = response.json()

print(f"Documents: {stats['document_count']}")
print(f"Total chunks: {stats['total_chunks']}")
print(f"Chat sessions: {stats['chat_sessions']}")
```

### Response:
```json
{
  "user_id": 123,
  "document_count": 5,
  "total_chunks": 75,
  "chat_sessions": 3,
  "document_status": {
    "completed": 4,
    "processing": 1,
    "failed": 0
  },
  "supported_formats": 12
}
```

## 9. Health Check

**Endpoint:** `GET /rag/health`

### cURL Example:
```bash
curl -X GET "http://localhost:8000/rag/health"
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/health"
response = requests.get(url)
health = response.json()

print(f"Status: {health['status']}")
for service, status in health['services'].items():
    print(f"  {service}: {'✅' if status else '❌'}")
```

### Response:
```json
{
  "status": "healthy",
  "services": {
    "openai_embeddings": true,
    "openai_chat": true,
    "pinecone": true,
    "database": true
  },
  "timestamp": "2025-01-15T10:00:00Z"
}
```

## Complete Workflow Example

Here's a complete Python example showing the full workflow:

```python
import requests
import time

# Configuration
BASE_URL = "http://localhost:8000"
TOKEN = "your_jwt_token_here"
USER_ID = 123

headers = {"Authorization": f"Bearer {TOKEN}"}

# 1. Upload a document
print("1. Uploading document...")
with open("sample_document.txt", "w") as f:
    f.write("""
    Python is a high-level programming language created by Guido van Rossum.
    It was first released in 1991 and is known for its simplicity and readability.
    
    Key features:
    - Easy to learn and use
    - Object-oriented programming
    - Large standard library
    - Cross-platform compatibility
    """)

files = {"file": open("sample_document.txt", "rb")}
data = {"title": "Python Guide", "description": "Basic Python information"}

response = requests.post(f"{BASE_URL}/rag/upload", headers=headers, files=files, data=data)
document = response.json()
print(f"✅ Document uploaded: {document['title']} ({document['chunks_count']} chunks)")

# Wait for processing
time.sleep(2)

# 2. Ask a question
print("\n2. Asking a question...")
query_data = {
    "user_id": USER_ID,
    "query": "Who created Python and when was it released?",
    "max_results": 3
}

response = requests.post(f"{BASE_URL}/rag/query", headers=headers, json=query_data)
result = response.json()
print(f"✅ Question: {result['query']}")
print(f"✅ Answer: {result['answer']}")
print(f"✅ Sources: {len(result['sources'])}")

# 3. List documents
print("\n3. Listing documents...")
response = requests.get(f"{BASE_URL}/rag/documents", headers=headers)
documents = response.json()
print(f"✅ Found {len(documents)} documents")

# 4. Get stats
print("\n4. Getting statistics...")
response = requests.get(f"{BASE_URL}/rag/stats", headers=headers)
stats = response.json()
print(f"✅ Total documents: {stats['document_count']}")
print(f"✅ Total chunks: {stats['total_chunks']}")

print("\n🎉 RAG system workflow completed successfully!")
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Unsupported file format. Supported formats: pdf, txt, docx, csv, xlsx, pptx, json, md"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Document not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Error processing document: [error message]"
}
```

## Notes

1. **File Size Limit**: Maximum file size is 50MB
2. **Supported Formats**: PDF, DOCX, TXT, CSV, XLSX, PPTX, JSON, MD
3. **Authentication**: All endpoints except health check and supported formats require authentication
4. **Rate Limits**: Consider implementing rate limiting for production use
5. **Session Management**: Use session_id to maintain conversation context
6. **User Isolation**: Each user's documents are stored in separate namespaces

## Testing with Postman

Import the provided `ScalebuildAI_Postman_Collection.json` and add these RAG endpoints to test the system easily.