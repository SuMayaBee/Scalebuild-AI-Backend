# Website RAG Processing API Examples

## 🌐 Website Processing with LangChain WebBaseLoader

The RAG system now supports processing websites using LangChain's WebBaseLoader. This allows you to scrape content from websites and ask questions based on that content.

---

## 1. 🌐 Process Single Website

**Endpoint:** `POST /rag/process-website`  
**Content-Type:** `application/json`

### Request Body:
```json
{
  "url": "https://example.com",
  "title": "Example Website Content",
  "verify_ssl": true,
  "max_pages": 1
}
```

### cURL Example:
```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://python.org/about/",
    "title": "Python.org About Page",
    "verify_ssl": true,
    "max_pages": 1
  }'
```

### Python Example:
```python
import requests

url = "http://localhost:8000/rag/process-website"
headers = {
    "Authorization": "Bearer your_jwt_token",
    "Content-Type": "application/json"
}

data = {
    "url": "https://python.org/about/",
    "title": "Python.org About Page",
    "verify_ssl": True,
    "max_pages": 1
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print(f"Website processed: {result['title']}")
print(f"Chunks created: {result['chunks_count']}")
print(f"Status: {result['status']}")
```

### Response:
```json
{
  "id": 3,
  "user_id": 1,
  "title": "Python.org About Page",
  "url": "https://python.org/about/",
  "file_type": "website",
  "chunks_count": 8,
  "status": "completed",
  "scraped_pages": 1,
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:01:00Z"
}
```

---

## 2. 🌐 Process Multiple Pages from Website

**Process multiple pages from the same domain:**

```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.python.org/3/",
    "title": "Python Documentation",
    "verify_ssl": true,
    "max_pages": 5
  }'
```

---

## 3. 🔍 Query Website Content

After processing a website, you can ask questions about its content:

```bash
curl -X POST "http://localhost:8000/rag/query" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "query": "What is Python used for according to the website?",
    "max_results": 5
  }'
```

---

## 🧪 Test Website Processing

Let's test with some popular websites:

### Test 1: Process Wikipedia Page
```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "title": "Wikipedia - Artificial Intelligence",
    "verify_ssl": true,
    "max_pages": 1
  }'
```

### Test 2: Process News Article
```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "title": "Example Website",
    "verify_ssl": true,
    "max_pages": 1
  }'
```

### Test 3: Process Documentation Site
```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://fastapi.tiangolo.com/",
    "title": "FastAPI Documentation",
    "verify_ssl": true,
    "max_pages": 3
  }'
```

---

## 🔄 Complete Website RAG Workflow

Here's a complete workflow example:

### Step 1: Process a website
```bash
# Process Python.org about page
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://python.org/about/",
    "title": "Python.org About Page",
    "verify_ssl": true,
    "max_pages": 1
  }'
```

### Step 2: Wait for processing (usually 5-10 seconds)
```bash
sleep 5
```

### Step 3: Ask questions about the website content
```bash
# Ask about Python's history
curl -X POST "http://localhost:8000/rag/query" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "query": "What is Python and what makes it special according to the website?",
    "max_results": 3
  }'

# Ask about Python's applications
curl -X POST "http://localhost:8000/rag/query" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "query": "What are the main applications of Python mentioned on the website?",
    "max_results": 3
  }'
```

### Step 4: Check your documents
```bash
curl -X GET "http://localhost:8000/rag/documents" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno"
```

---

## 🎯 Expected Responses

### Website Processing Response:
```json
{
  "id": 3,
  "user_id": 1,
  "title": "Python.org About Page",
  "url": "https://python.org/about/",
  "file_type": "website",
  "chunks_count": 8,
  "status": "completed",
  "scraped_pages": 1,
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:01:00Z"
}
```

### Query Response with Website Content:
```json
{
  "query": "What is Python and what makes it special according to the website?",
  "answer": "According to the website, Python is a programming language that lets you work quickly and integrate systems more effectively. Python is known for its simplicity, readability, and versatility, making it suitable for web development, data analysis, artificial intelligence, and scientific computing.",
  "sources": [
    {
      "content": "Python is a programming language that lets you work quickly and integrate systems more effectively...",
      "metadata": {
        "document_id": 3,
        "source_url": "https://python.org/about/",
        "title": "Python.org About Page",
        "chunk_index": 0,
        "score": 0.89
      },
      "score": 0.89
    }
  ],
  "session_id": "website-chat-session-456",
  "processing_time": 3.21,
  "tokens_used": 320
}
```

---

## 🔧 Advanced Features

### Process with SSL Verification Disabled:
```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://self-signed-cert-site.com",
    "title": "Site with Self-Signed Certificate",
    "verify_ssl": false,
    "max_pages": 1
  }'
```

### Process Multiple Pages from a Site:
```bash
curl -X POST "http://localhost:8000/rag/process-website" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.example.com",
    "title": "Documentation Site",
    "verify_ssl": true,
    "max_pages": 10
  }'
```

---

## 📝 Parameters Explained

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | required | The website URL to process |
| `title` | string | optional | Custom title for the document |
| `verify_ssl` | boolean | true | Whether to verify SSL certificates |
| `max_pages` | integer | 1 | Maximum number of pages to scrape from the site |

---

## 🚨 Important Notes

1. **Rate Limiting**: Be respectful of websites' rate limits
2. **Robots.txt**: The system respects robots.txt when possible
3. **Content Size**: Large websites may take longer to process
4. **SSL Issues**: Use `verify_ssl: false` for sites with certificate issues
5. **JavaScript**: Static content only - JavaScript-rendered content may not be captured
6. **Legal**: Ensure you have permission to scrape the websites you're processing

---

## 🔍 Troubleshooting

### Common Issues:

1. **SSL Certificate Error**:
   - Set `verify_ssl: false` in the request

2. **Website Blocks Scraping**:
   - Some sites block automated requests
   - Try different URLs or contact site owners

3. **No Content Extracted**:
   - Website might be JavaScript-heavy
   - Try a different page or use a different approach

4. **Timeout Errors**:
   - Reduce `max_pages` parameter
   - Try processing one page at a time

---

## 🎉 Success!

Your RAG system now supports both document uploads and website processing using LangChain's WebBaseLoader. You can:

1. ✅ Upload documents (PDF, DOCX, TXT, etc.)
2. ✅ Process websites and web pages
3. ✅ Ask questions about both document and website content
4. ✅ Get answers with source citations
5. ✅ Maintain chat history and sessions

Start by processing a simple website like `https://example.com` and then ask questions about its content!