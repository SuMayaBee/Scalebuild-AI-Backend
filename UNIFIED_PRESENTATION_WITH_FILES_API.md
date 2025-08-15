# 🎯 Unified Presentation Generation API with File Uploads

## 🚀 Updated Unified Endpoint

**Endpoint:** `POST /presentation/generate-unified`  
**Content-Type:** `multipart/form-data`  
**Authentication:** Required (JWT Bearer Token)

This endpoint now supports **file uploads** for context documents, combining outline generation, slide creation, RAG context integration, and AI image generation into a single powerful API call.

---

## 📋 Request Parameters

### **Required Fields:**
- `slides_count` (integer, 3-20): Number of slides to generate
- `prompt` (string, min 10 chars): Main presentation topic/prompt

### **Optional Form Fields:**
- `color_theme` (string): Presentation color theme (default: "default")
- `website_urls` (string): Comma-separated website URLs for context
- `industry_sector` (string): Industry sector information
- `one_line_pitch` (string): One-line pitch
- `problem_solving` (string): Problem you're solving
- `unique_solution` (string): Your unique solution
- `target_audience` (string): Target audience
- `business_model` (string): Business model
- `revenue_plan` (string): Revenue plan
- `competitors` (string): Competitors analysis
- `vision` (string): Company/project vision
- `language` (string): Presentation language (default: "English")
- `tone` (string): Presentation tone (default: "Professional")
- `generate_images` (boolean): Generate AI images (default: true)

### **File Upload Field:**
- `context_files` (files[]): Multiple document files for context (PDF, DOCX, TXT, CSV, XLSX, PPTX, JSON, MD)

---

## 🎯 Complete Request Examples

### **Example 1: Basic Presentation with Document Upload**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -F "slides_count=8" \
  -F "prompt=AI-Powered Healthcare Solutions for Remote Patient Monitoring" \
  -F "color_theme=modern" \
  -F "language=English" \
  -F "tone=Professional" \
  -F "generate_images=true" \
  -F "context_files=@healthcare_research.pdf" \
  -F "context_files=@market_analysis.docx"
```

### **Example 2: Business Pitch with Multiple Context Sources**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -F "slides_count=12" \
  -F "prompt=Revolutionary EdTech Platform for Personalized Learning" \
  -F "color_theme=corporate" \
  -F "industry_sector=Education Technology" \
  -F "one_line_pitch=AI-powered personalized learning platform that adapts to each student's learning style and pace" \
  -F "problem_solving=Traditional one-size-fits-all education fails to address individual learning differences" \
  -F "unique_solution=Our AI analyzes learning patterns and creates personalized curricula that adapt in real-time" \
  -F "target_audience=K-12 schools, homeschooling families, and online education providers" \
  -F "business_model=SaaS subscription model with tiered pricing for institutions and individual learners" \
  -F "revenue_plan=Freemium model with premium features, targeting $10M ARR by year 3" \
  -F "competitors=Khan Academy, Coursera, and traditional LMS providers like Blackboard" \
  -F "vision=To democratize personalized education and make adaptive learning accessible to every student worldwide" \
  -F "website_urls=https://en.wikipedia.org/wiki/Educational_technology,https://www.khanacademy.org" \
  -F "context_files=@education_market_report.pdf" \
  -F "context_files=@competitor_analysis.xlsx" \
  -F "context_files=@user_research_findings.docx"
```

### **Example 3: Research Presentation with Academic Papers**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -F "slides_count=15" \
  -F "prompt=Climate Change Impact on Coastal Cities" \
  -F "color_theme=minimal" \
  -F "industry_sector=Environmental Science" \
  -F "website_urls=https://en.wikipedia.org/wiki/Sea_level_rise" \
  -F "language=English" \
  -F "tone=Academic" \
  -F "generate_images=true" \
  -F "context_files=@ipcc_report_chapter.pdf" \
  -F "context_files=@coastal_cities_data.csv" \
  -F "context_files=@research_methodology.txt"
```

### **Example 4: Startup Pitch with Financial Data**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -F "slides_count=10" \
  -F "prompt=Series A Funding Pitch for FinTech Startup" \
  -F "color_theme=corporate" \
  -F "industry_sector=Financial Technology" \
  -F "one_line_pitch=AI-powered personal finance advisor for Gen Z" \
  -F "problem_solving=Young adults lack financial literacy and personalized guidance" \
  -F "unique_solution=Gamified AI advisor that learns spending patterns and provides real-time guidance" \
  -F "target_audience=18-28 year olds with disposable income" \
  -F "business_model=Freemium with premium financial planning features" \
  -F "revenue_plan=Subscription revenue + affiliate partnerships with financial institutions" \
  -F "competitors=Mint, YNAB, Personal Capital" \
  -F "vision=Democratize financial wellness for the next generation" \
  -F "context_files=@financial_projections.xlsx" \
  -F "context_files=@market_research.pdf" \
  -F "context_files=@user_personas.docx" \
  -F "context_files=@competitive_landscape.pptx"
```

---

## 📊 Response Structure

### **Successful Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION><SECTION layout=\"left\">...</SECTION></PRESENTATION>",
  "slides_count": 12,
  "processing_time": 67.89,
  "generated_images": [
    {
      "query": "modern educational technology classroom with AI-powered learning interfaces",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345678.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    },
    {
      "query": "personalized learning dashboard showing adaptive curriculum paths",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_2_1642345679.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 2
    }
  ],
  "context_sources_used": [
    {
      "type": "website",
      "url": "https://en.wikipedia.org/wiki/Educational_technology",
      "title": "Educational Technology Overview",
      "chunks_count": 8,
      "summary": "Educational technology encompasses digital tools and platforms..."
    },
    {
      "type": "document",
      "filename": "education_market_report.pdf",
      "title": "Context: education_market_report.pdf",
      "chunks_count": 12,
      "file_type": "pdf",
      "file_size": 156789,
      "summary": "The global education technology market is projected to reach..."
    },
    {
      "type": "document",
      "filename": "competitor_analysis.xlsx",
      "title": "Context: competitor_analysis.xlsx",
      "chunks_count": 5,
      "file_type": "xlsx",
      "file_size": 45123,
      "summary": "Analysis of key competitors shows Khan Academy leads in..."
    }
  ],
  "prompt": "Revolutionary EdTech Platform for Personalized Learning",
  "theme": "corporate",
  "language": "English",
  "tone": "Professional"
}
```

---

## 🎯 Python SDK Example with File Uploads

```python
import requests
from pathlib import Path

class UnifiedPresentationClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {token}"}
    
    def generate_presentation_with_files(
        self,
        slides_count: int,
        prompt: str,
        context_files: list = None,
        **kwargs
    ) -> dict:
        """Generate unified presentation with file uploads"""
        
        # Prepare form data
        data = {
            "slides_count": slides_count,
            "prompt": prompt,
            **kwargs
        }
        
        # Prepare files for upload
        files = []
        if context_files:
            for file_path in context_files:
                file_path = Path(file_path)
                if file_path.exists():
                    files.append(
                        ("context_files", (file_path.name, open(file_path, "rb")))
                    )
        
        try:
            response = requests.post(
                f"{self.base_url}/presentation/generate-unified",
                headers=self.headers,
                data=data,
                files=files
            )
            
            return response.json()
            
        finally:
            # Close all opened files
            for _, (_, file_obj) in files:
                file_obj.close()

# Usage example
client = UnifiedPresentationClient(
    base_url="http://localhost:8000",
    token="your_jwt_token_here"
)

# Generate presentation with multiple document types
result = client.generate_presentation_with_files(
    slides_count=10,
    prompt="AI Startup Investment Pitch",
    color_theme="corporate",
    industry_sector="Artificial Intelligence",
    one_line_pitch="Revolutionary AI that understands human emotions",
    problem_solving="Current AI lacks emotional intelligence",
    unique_solution="Proprietary emotion recognition creates empathetic interactions",
    target_audience="Enterprise customers and consumer app developers",
    business_model="API-as-a-Service with usage-based pricing",
    revenue_plan="$5M ARR by year 2 through enterprise partnerships",
    website_urls="https://example.com/ai-research,https://techcrunch.com/ai-trends",
    context_files=[
        "business_plan.pdf",
        "financial_projections.xlsx", 
        "market_research.docx",
        "technical_specifications.txt",
        "user_feedback.csv"
    ],
    generate_images=True
)

if result["success"]:
    print(f"✅ Presentation generated with {result['slides_count']} slides")
    print(f"⏱️ Processing time: {result['processing_time']:.2f}s")
    print(f"🖼️ Generated {len(result['generated_images'])} images")
    print(f"📚 Used {len(result['context_sources_used'])} context sources")
    
    # Show context sources used
    for source in result['context_sources_used']:
        if source['type'] == 'document':
            print(f"📄 Document: {source['filename']} ({source['file_type']}) - {source['chunks_count']} chunks")
        elif source['type'] == 'website':
            print(f"🌐 Website: {source['url']} - {source['chunks_count']} chunks")
    
    # Save XML to file
    with open("presentation.xml", "w", encoding="utf-8") as f:
        f.write(result["presentation_xml"])
        
    print("💾 Presentation saved to presentation.xml")
else:
    print(f"❌ Error: {result['error']}")
```

---

## 📁 Supported File Types for Context Documents

| File Type | Extensions | Description |
|-----------|------------|-------------|
| **PDF** | .pdf | PDF documents |
| **Word** | .docx, .doc | Microsoft Word documents |
| **Excel** | .xlsx, .xls | Excel spreadsheets with data |
| **PowerPoint** | .pptx, .ppt | PowerPoint presentations |
| **Text** | .txt, .md | Plain text and Markdown files |
| **CSV** | .csv | Comma-separated data files |
| **JSON** | .json | Structured JSON data |

---

## 🔧 Advanced Use Cases

### **1. Academic Research Presentation**
```bash
# Upload research papers, data files, and methodology documents
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer $TOKEN" \
  -F "slides_count=15" \
  -F "prompt=Machine Learning Applications in Medical Diagnosis" \
  -F "tone=Academic" \
  -F "industry_sector=Healthcare AI" \
  -F "context_files=@research_paper_1.pdf" \
  -F "context_files=@research_paper_2.pdf" \
  -F "context_files=@dataset_analysis.csv" \
  -F "context_files=@methodology.txt" \
  -F "website_urls=https://pubmed.ncbi.nlm.nih.gov/relevant-studies"
```

### **2. Business Strategy Presentation**
```bash
# Upload market analysis, financial data, and strategic documents
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer $TOKEN" \
  -F "slides_count=12" \
  -F "prompt=Q4 Business Strategy and Market Expansion" \
  -F "color_theme=corporate" \
  -F "context_files=@market_analysis_q3.xlsx" \
  -F "context_files=@competitor_report.pdf" \
  -F "context_files=@financial_performance.csv" \
  -F "context_files=@strategic_initiatives.docx" \
  -F "business_model=B2B SaaS with enterprise focus" \
  -F "target_audience=C-level executives and board members"
```

### **3. Product Launch Presentation**
```bash
# Upload product specs, user research, and marketing materials
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer $TOKEN" \
  -F "slides_count=10" \
  -F "prompt=Revolutionary Smart Home Security System Launch" \
  -F "color_theme=modern" \
  -F "context_files=@product_specifications.pdf" \
  -F "context_files=@user_research_findings.docx" \
  -F "context_files=@market_positioning.pptx" \
  -F "context_files=@pricing_strategy.xlsx" \
  -F "unique_solution=AI-powered security that learns family patterns" \
  -F "target_audience=Homeowners aged 30-55 with household income >$75k"
```

---

## ⚡ Performance & Limits

| Feature | Limit | Notes |
|---------|-------|-------|
| **Slides Count** | 3-20 | Optimal range for presentations |
| **Website URLs** | 10 max | Comma-separated in single field |
| **Context Files** | 10 max | Multiple file uploads supported |
| **File Size** | 50MB each | Per uploaded file |
| **Total Upload** | 200MB | Combined size of all files |
| **Processing Time** | 60-180s | Depends on files and complexity |
| **Image Generation** | 5 max | To balance quality and speed |

---

## 🚨 Error Handling

### **File Upload Errors:**
```json
{
  "success": false,
  "error": "Error processing file document.pdf: Unsupported file format",
  "context_sources_used": [
    {
      "type": "document",
      "filename": "document.pdf",
      "error": "Unsupported file format"
    }
  ]
}
```

### **Processing Errors:**
```json
{
  "success": false,
  "error": "RAG processing failed for uploaded documents",
  "processing_time": 15.67,
  "context_sources_used": []
}
```

---

## 🎉 Key Features Summary

The **Updated Unified Presentation API** now supports:

1. ✅ **File Upload Integration** (PDF, DOCX, XLSX, PPTX, TXT, CSV, JSON, MD)
2. ✅ **Multi-Document Processing** (Up to 10 files per request)
3. ✅ **RAG Context Extraction** (Automatic text extraction and summarization)
4. ✅ **Website URL Integration** (Combine files with web content)
5. ✅ **Business Information Processing** (Comprehensive business context)
6. ✅ **AI Image Generation** (DALL-E 3 with contextual prompts)
7. ✅ **Multi-language Support** (Global presentation generation)
8. ✅ **Comprehensive Error Handling** (Detailed error reporting)

This enhanced endpoint provides the most comprehensive presentation generation solution, combining uploaded documents, web content, business information, and AI-powered content creation in a single API call! 🚀