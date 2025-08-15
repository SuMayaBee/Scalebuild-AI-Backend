# 🎯 Unified Presentation Generation API (No Authentication Required)

## 🚀 Public Access Unified Endpoint

**Endpoint:** `POST /presentation/generate-unified`  
**Content-Type:** `multipart/form-data`  
**Authentication:** ❌ **NOT REQUIRED** (Public Access)

This endpoint provides **public access** to the unified presentation generation system, combining outline generation, slide creation, RAG context integration, and AI image generation without requiring authentication.

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

## 🎯 Complete Request Examples (No Auth Required)

### **Example 1: Basic Presentation with Document Upload**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
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

### **Example 4: Simple Presentation (Minimal Parameters)**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=6" \
  -F "prompt=Introduction to Machine Learning"
```

### **Example 5: Website Context Only (No File Uploads)**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=10" \
  -F "prompt=Sustainable Energy Solutions for Smart Cities" \
  -F "website_urls=https://en.wikipedia.org/wiki/Smart_city,https://en.wikipedia.org/wiki/Renewable_energy" \
  -F "industry_sector=Clean Energy & Smart Infrastructure" \
  -F "target_audience=City planners, government officials, and infrastructure investors"
```

---

## 📊 Response Structure (Same as Before)

### **Successful Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION><SECTION layout=\"left\">...</SECTION></PRESENTATION>",
  "slides_count": 8,
  "processing_time": 45.67,
  "generated_images": [
    {
      "query": "modern healthcare AI technology with doctors and digital interfaces",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345678.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    }
  ],
  "context_sources_used": [
    {
      "type": "document",
      "filename": "healthcare_research.pdf",
      "title": "Context: healthcare_research.pdf",
      "chunks_count": 5,
      "file_type": "pdf",
      "file_size": 156789,
      "summary": "Healthcare AI research shows significant improvements in patient outcomes..."
    }
  ],
  "prompt": "AI-Powered Healthcare Solutions for Remote Patient Monitoring",
  "theme": "modern",
  "language": "English",
  "tone": "Professional"
}
```

---

## 🎯 Python SDK Example (No Authentication)

```python
import requests
from pathlib import Path

class PublicPresentationClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        # No authentication headers needed!
    
    def generate_presentation_with_files(
        self,
        slides_count: int,
        prompt: str,
        context_files: list = None,
        **kwargs
    ) -> dict:
        """Generate unified presentation with file uploads (no auth required)"""
        
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
                data=data,  # No headers needed!
                files=files
            )
            
            return response.json()
            
        finally:
            # Close all opened files
            for _, (_, file_obj) in files:
                file_obj.close()

# Usage example (No token required!)
client = PublicPresentationClient(base_url="http://localhost:8000")

# Generate presentation without authentication
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
        "market_research.docx"
    ],
    generate_images=True
)

if result["success"]:
    print(f"✅ Presentation generated with {result['slides_count']} slides")
    print(f"⏱️ Processing time: {result['processing_time']:.2f}s")
    print(f"🖼️ Generated {len(result['generated_images'])} images")
    print(f"📚 Used {len(result['context_sources_used'])} context sources")
    
    # Save XML to file
    with open("presentation.xml", "w", encoding="utf-8") as f:
        f.write(result["presentation_xml"])
        
    print("💾 Presentation saved to presentation.xml")
else:
    print(f"❌ Error: {result['error']}")
```

---

## 🌐 JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function generatePresentation() {
    const form = new FormData();
    
    // Required fields
    form.append('slides_count', '8');
    form.append('prompt', 'AI-Powered Healthcare Solutions');
    
    // Optional fields
    form.append('color_theme', 'modern');
    form.append('industry_sector', 'Healthcare Technology');
    form.append('one_line_pitch', 'Revolutionary AI for patient monitoring');
    form.append('generate_images', 'true');
    
    // File uploads
    if (fs.existsSync('healthcare_research.pdf')) {
        form.append('context_files', fs.createReadStream('healthcare_research.pdf'));
    }
    if (fs.existsSync('market_analysis.docx')) {
        form.append('context_files', fs.createReadStream('market_analysis.docx'));
    }
    
    try {
        const response = await axios.post(
            'http://localhost:8000/presentation/generate-unified',
            form,
            {
                headers: {
                    ...form.getHeaders()
                    // No Authorization header needed!
                }
            }
        );
        
        console.log('✅ Presentation generated successfully!');
        console.log(`Slides: ${response.data.slides_count}`);
        console.log(`Processing time: ${response.data.processing_time}s`);
        console.log(`Images generated: ${response.data.generated_images.length}`);
        
        // Save XML to file
        fs.writeFileSync('presentation.xml', response.data.presentation_xml);
        console.log('💾 Presentation saved to presentation.xml');
        
    } catch (error) {
        console.error('❌ Error:', error.response?.data || error.message);
    }
}

generatePresentation();
```

---

## 🔧 Frontend Integration Examples

### **HTML Form Example:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Presentation Generator</title>
</head>
<body>
    <h1>Generate Presentation</h1>
    <form action="http://localhost:8000/presentation/generate-unified" method="post" enctype="multipart/form-data">
        <!-- Required Fields -->
        <label>Number of Slides (3-20):</label>
        <input type="number" name="slides_count" min="3" max="20" value="8" required><br><br>
        
        <label>Presentation Topic:</label>
        <input type="text" name="prompt" placeholder="Enter your presentation topic" required><br><br>
        
        <!-- Optional Fields -->
        <label>Color Theme:</label>
        <select name="color_theme">
            <option value="default">Default</option>
            <option value="modern">Modern</option>
            <option value="corporate">Corporate</option>
            <option value="minimal">Minimal</option>
        </select><br><br>
        
        <label>Industry Sector:</label>
        <input type="text" name="industry_sector" placeholder="e.g., Technology, Healthcare"><br><br>
        
        <label>One-Line Pitch:</label>
        <input type="text" name="one_line_pitch" placeholder="Describe your solution in one line"><br><br>
        
        <label>Problem You're Solving:</label>
        <textarea name="problem_solving" placeholder="What problem does this address?"></textarea><br><br>
        
        <label>Your Unique Solution:</label>
        <textarea name="unique_solution" placeholder="How do you solve it uniquely?"></textarea><br><br>
        
        <label>Target Audience:</label>
        <input type="text" name="target_audience" placeholder="Who is your target audience?"><br><br>
        
        <label>Website URLs (comma-separated):</label>
        <input type="text" name="website_urls" placeholder="https://example.com, https://another.com"><br><br>
        
        <label>Upload Context Documents:</label>
        <input type="file" name="context_files" multiple accept=".pdf,.docx,.txt,.csv,.xlsx,.pptx,.json,.md"><br><br>
        
        <label>Language:</label>
        <select name="language">
            <option value="English">English</option>
            <option value="Spanish">Spanish</option>
            <option value="French">French</option>
            <option value="German">German</option>
        </select><br><br>
        
        <label>Tone:</label>
        <select name="tone">
            <option value="Professional">Professional</option>
            <option value="Casual">Casual</option>
            <option value="Academic">Academic</option>
            <option value="Creative">Creative</option>
        </select><br><br>
        
        <label>
            <input type="checkbox" name="generate_images" value="true" checked>
            Generate AI Images
        </label><br><br>
        
        <button type="submit">Generate Presentation</button>
    </form>
</body>
</html>
```

---

## ⚡ Quick Test Commands

### **Minimal Test (Just Required Fields):**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=5" \
  -F "prompt=Introduction to Artificial Intelligence"
```

### **With Business Context:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=8" \
  -F "prompt=Startup Pitch for AI Company" \
  -F "industry_sector=Artificial Intelligence" \
  -F "one_line_pitch=AI that makes everyone more productive" \
  -F "problem_solving=People waste time on repetitive tasks" \
  -F "unique_solution=Our AI automates 80% of routine work"
```

### **With Website Context:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=10" \
  -F "prompt=Climate Change Solutions" \
  -F "website_urls=https://en.wikipedia.org/wiki/Climate_change"
```

---

## 🎯 Key Benefits of No Authentication

1. ✅ **Easy Integration**: No token management required
2. ✅ **Public Access**: Anyone can use the API
3. ✅ **Simplified Testing**: Direct cURL commands work immediately
4. ✅ **Frontend Friendly**: Easy HTML form integration
5. ✅ **Rapid Prototyping**: Quick testing and development
6. ✅ **Demo Ready**: Perfect for demonstrations and trials

---

## 🚨 Important Notes

1. **Public Access**: This endpoint is now publicly accessible without authentication
2. **Rate Limiting**: Consider implementing rate limiting for production use
3. **Resource Usage**: Monitor usage as anyone can generate presentations
4. **File Uploads**: Still supports all document types and processing
5. **Full Functionality**: All features work the same, just without auth requirement

---

## 🎉 Summary

The **Unified Presentation Generation API** now provides **public access** with:

1. ✅ **No Authentication Required** (Public endpoint)
2. ✅ **File Upload Support** (PDF, DOCX, XLSX, PPTX, TXT, CSV, JSON, MD)
3. ✅ **RAG Context Integration** (Website + Document processing)
4. ✅ **Business Information Processing** (Comprehensive business context)
5. ✅ **AI Image Generation** (DALL-E 3 with contextual prompts)
6. ✅ **Multi-language Support** (Global presentation generation)
7. ✅ **Easy Integration** (HTML forms, JavaScript, Python, cURL)

Perfect for public demos, trials, and easy integration! 🚀