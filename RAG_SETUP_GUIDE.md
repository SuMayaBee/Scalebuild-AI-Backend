# RAG System Setup Guide

## Overview
The RAG (Retrieval-Augmented Generation) system allows users to upload documents and ask questions based on the content of those documents. It uses Pinecone for vector storage, OpenAI for embeddings and chat completion, and supports multiple file formats.

## Features
- **Document Upload**: Support for PDF, DOCX, TXT, CSV, XLSX, PPTX, JSON, MD files
- **Text Processing**: Automatic text extraction and chunking
- **Vector Storage**: Pinecone vector database for semantic search
- **AI Chat**: GPT-powered question answering based on uploaded documents
- **Chat History**: Persistent chat sessions with source citations
- **User Isolation**: Each user's documents are stored in separate namespaces

## Setup Instructions

### 1. Environment Variables
Add these variables to your `.env` file:

```bash
# RAG System Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=scalebuild-rag

# OpenAI API Key (already configured)
OPENAI_API_KEY=your_openai_api_key
```

### 2. Get Pinecone API Key
1. Sign up at [Pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Get your API key from the dashboard
4. Replace `your_pinecone_api_key_here` in the `.env` file

### 3. Database Migration
The RAG tables have already been created with the migration:
```bash
alembic upgrade head
```

### 4. Install Dependencies
All required dependencies are already installed:
- pinecone-client
- PyPDF2
- pandas
- openpyxl
- python-pptx

## API Endpoints

### Upload Document
```http
POST /rag/upload
Content-Type: multipart/form-data

file: [document file]
title: "Optional document title"
description: "Optional description"
```

### Query Documents
```http
POST /rag/query
Content-Type: application/json

{
  "user_id": 1,
  "query": "What is Python?",
  "session_id": "optional-session-id",
  "max_results": 5,
  "include_sources": true
}
```

### List Documents
```http
GET /rag/documents?skip=0&limit=100
```

### Delete Document
```http
DELETE /rag/documents/{document_id}
```

### Get Chat History
```http
GET /rag/chat/{session_id}
```

### List Chat Sessions
```http
GET /rag/chat/sessions?skip=0&limit=50
```

### Get Supported Formats
```http
GET /rag/supported-formats
```

### Health Check
```http
GET /rag/health
```

### User Statistics
```http
GET /rag/stats
```

## Supported File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | .pdf | PDF documents |
| Word | .docx | Microsoft Word documents |
| Text | .txt, .md | Plain text and Markdown files |
| Excel | .xlsx, .xls | Excel spreadsheets |
| CSV | .csv | Comma-separated values |
| PowerPoint | .pptx | PowerPoint presentations |
| JSON | .json | JSON data files |

## Usage Examples

### 1. Upload a Document
```python
import requests

files = {'file': open('document.pdf', 'rb')}
data = {'title': 'My Document', 'description': 'Important document'}
headers = {'Authorization': 'Bearer your_jwt_token'}

response = requests.post(
    'http://localhost:8000/rag/upload',
    files=files,
    data=data,
    headers=headers
)
```

### 2. Ask a Question
```python
import requests

data = {
    "user_id": 1,
    "query": "What are the main points in the document?",
    "max_results": 5
}
headers = {'Authorization': 'Bearer your_jwt_token'}

response = requests.post(
    'http://localhost:8000/rag/query',
    json=data,
    headers=headers
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {len(result['sources'])} documents")
```

## Testing

Run the test script to verify everything is working:

```bash
python test_rag_system.py
```

This will test:
- Document processing
- Embedding generation
- Vector operations (if Pinecone is configured)
- Full RAG workflow (if all services are configured)

## Architecture

```
User Upload → Document Processor → Text Chunking → OpenAI Embeddings → Pinecone Storage
                                                                              ↓
User Query → OpenAI Embeddings → Pinecone Search → Context Retrieval → GPT Answer
```

## Troubleshooting

### Common Issues

1. **Pinecone API Key Error**
   - Make sure you've set the correct API key in `.env`
   - Verify your Pinecone account is active

2. **OpenAI API Error**
   - Check your OpenAI API key and billing status
   - Ensure you have sufficient credits

3. **File Upload Errors**
   - Check file size (max 50MB)
   - Verify file format is supported
   - Ensure file is not corrupted

4. **Database Errors**
   - Run `alembic upgrade head` to ensure tables exist
   - Check database connection string

### Performance Tips

1. **Chunk Size**: Adjust chunk size based on your documents
   - Smaller chunks (500-1000 chars) for precise answers
   - Larger chunks (1500-2000 chars) for more context

2. **Max Results**: Limit search results for faster responses
   - Use 3-5 results for most queries
   - Increase for complex questions requiring more context

3. **Namespace Management**: Each user gets their own namespace
   - Ensures data isolation
   - Improves search performance

## Security

- User authentication required for all endpoints
- Documents isolated by user namespace
- File size and type validation
- SQL injection protection with SQLAlchemy ORM

## Monitoring

Check system health with:
```http
GET /rag/health
```

Monitor user statistics with:
```http
GET /rag/stats
```

## Next Steps

1. Set up your Pinecone API key
2. Test with the provided test script
3. Upload your first document
4. Start asking questions!

For support, check the logs or run the health check endpoint to diagnose issues.