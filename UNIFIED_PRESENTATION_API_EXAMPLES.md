# 🎯 Unified Presentation Generation API

## 🚀 New Unified Endpoint

**Endpoint:** `POST /presentation/generate-unified`  
**Content-Type:** `application/json`  
**Authentication:** Required (JWT Bearer Token)

This endpoint combines outline generation, slide creation, RAG context integration, and AI image generation into a single powerful API call.

---

## 📋 Request Body Structure

### **Required Fields:**
- `slides_count` (integer, 3-20): Number of slides to generate
- `prompt` (string, min 10 chars): Main presentation topic/prompt

### **Optional Fields:**
- `color_theme` (string): Presentation color theme (default: "default")
- `website_urls` (array): Website URLs for context extraction
- `context_sources` (array): Additional text context sources
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

---

## 🎯 Complete Request Examples

### **Example 1: Basic Presentation**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "slides_count": 8,
    "prompt": "AI-Powered Healthcare Solutions for Remote Patient Monitoring",
    "color_theme": "modern",
    "language": "English",
    "tone": "Professional",
    "generate_images": true
  }'
```

### **Example 2: Business Pitch with Context**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "slides_count": 10,
    "prompt": "Revolutionary EdTech Platform for Personalized Learning",
    "color_theme": "corporate",
    "industry_sector": "Education Technology",
    "one_line_pitch": "AI-powered personalized learning platform that adapts to each student'\''s learning style and pace",
    "problem_solving": "Traditional one-size-fits-all education fails to address individual learning differences, leading to poor engagement and outcomes",
    "unique_solution": "Our AI analyzes learning patterns and creates personalized curricula that adapt in real-time to optimize each student'\''s learning journey",
    "target_audience": "K-12 schools, homeschooling families, and online education providers",
    "business_model": "SaaS subscription model with tiered pricing for institutions and individual learners",
    "revenue_plan": "Freemium model with premium features, targeting $10M ARR by year 3",
    "competitors": "Khan Academy, Coursera, and traditional LMS providers like Blackboard",
    "vision": "To democratize personalized education and make adaptive learning accessible to every student worldwide",
    "language": "English",
    "tone": "Professional",
    "generate_images": true
  }'
```

### **Example 3: With Website Context Integration**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "slides_count": 12,
    "prompt": "Sustainable Energy Solutions for Smart Cities",
    "color_theme": "modern",
    "website_urls": [
      "https://en.wikipedia.org/wiki/Smart_city",
      "https://en.wikipedia.org/wiki/Renewable_energy"
    ],
    "context_sources": [
      "Smart cities integrate IoT sensors, data analytics, and sustainable infrastructure to optimize resource usage and improve quality of life for residents.",
      "Current energy consumption in urban areas accounts for 70% of global CO2 emissions, making sustainable energy solutions critical for climate goals."
    ],
    "industry_sector": "Clean Energy & Smart Infrastructure",
    "target_audience": "City planners, government officials, and infrastructure investors",
    "business_model": "B2B2C model partnering with municipalities to deploy smart energy grids",
    "language": "English",
    "tone": "Professional",
    "generate_images": true
  }'
```

### **Example 4: Multi-language Presentation**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJic3NlMTQ0NkBpaXQuZHUuYWMuYmQiLCJ1c2VyX2lkIjoxLCJleHAiOjE3NTU4MDQzMjV9.I2HZBw7xoRxYG3ukmqZRRtOQ16_QGC_bSEhZFMz1Fno" \
  -H "Content-Type: application/json" \
  -d '{
    "slides_count": 6,
    "prompt": "Inteligencia Artificial en la Medicina Moderna",
    "color_theme": "minimal",
    "industry_sector": "Tecnología Médica",
    "language": "Spanish",
    "tone": "Academic",
    "generate_images": true
  }'
```

---

## 📊 Response Structure

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
    },
    {
      "query": "futuristic medical monitoring devices and patient care technology",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_2_1642345679.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 2
    }
  ],
  "context_sources_used": [
    {
      "type": "website",
      "url": "https://example.com/healthcare-ai",
      "title": "Healthcare AI Trends",
      "chunks_count": 5,
      "summary": "AI in healthcare is transforming patient care through predictive analytics..."
    }
  ],
  "prompt": "AI-Powered Healthcare Solutions for Remote Patient Monitoring",
  "theme": "modern",
  "language": "English",
  "tone": "Professional"
}
```

### **Error Response:**
```json
{
  "success": false,
  "presentation_xml": null,
  "slides_count": 8,
  "processing_time": 12.34,
  "generated_images": [],
  "context_sources_used": [],
  "error": "Error message describing what went wrong",
  "prompt": "AI-Powered Healthcare Solutions",
  "theme": "modern",
  "language": "English",
  "tone": "Professional"
}
```

---

## 🎯 Python SDK Example

```python
import requests
import json

class UnifiedPresentationClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def generate_presentation(
        self,
        slides_count: int,
        prompt: str,
        **kwargs
    ) -> dict:
        """Generate unified presentation with RAG context"""
        
        payload = {
            "slides_count": slides_count,
            "prompt": prompt,
            **kwargs
        }
        
        response = requests.post(
            f"{self.base_url}/presentation/generate-unified",
            headers=self.headers,
            json=payload
        )
        
        return response.json()

# Usage example
client = UnifiedPresentationClient(
    base_url="http://localhost:8000",
    token="your_jwt_token_here"
)

# Generate business pitch presentation
result = client.generate_presentation(
    slides_count=10,
    prompt="Revolutionary AI Startup Pitch",
    color_theme="corporate",
    industry_sector="Artificial Intelligence",
    one_line_pitch="AI that understands human emotions and responds accordingly",
    problem_solving="Current AI lacks emotional intelligence, leading to poor user experiences",
    unique_solution="Our proprietary emotion recognition AI creates empathetic interactions",
    target_audience="Enterprise customers and consumer app developers",
    business_model="API-as-a-Service with usage-based pricing",
    revenue_plan="$5M ARR by year 2 through enterprise partnerships",
    website_urls=["https://example.com/ai-research"],
    context_sources=["Recent studies show 85% of users prefer emotionally aware AI interfaces"],
    generate_images=True
)

if result["success"]:
    print(f"✅ Presentation generated with {result['slides_count']} slides")
    print(f"⏱️ Processing time: {result['processing_time']:.2f}s")
    print(f"🖼️ Generated {len(result['generated_images'])} images")
    print(f"📚 Used {len(result['context_sources_used'])} context sources")
    
    # Save XML to file
    with open("presentation.xml", "w") as f:
        f.write(result["presentation_xml"])
else:
    print(f"❌ Error: {result['error']}")
```

---

## 🔧 Advanced Features

### **1. RAG Context Integration**
- **Website URLs**: Automatically scrapes and processes website content
- **Context Sources**: Integrates additional text-based context
- **Smart Summarization**: Uses RAG to extract relevant information

### **2. Business Information Integration**
- **Industry Context**: Tailors content to specific industry sectors
- **Business Model**: Incorporates business model information
- **Competitive Analysis**: Includes competitor information in slides

### **3. AI Image Generation**
- **Contextual Images**: Generates images based on slide content
- **Professional Quality**: DALL-E 3 for high-quality visuals
- **Landscape Format**: Optimized 1792x1024 for presentations

### **4. Multi-language Support**
- **Global Reach**: Supports multiple languages
- **Cultural Adaptation**: Tone and style adapted to language/culture

---

## ⚡ Performance & Limits

| Feature | Limit | Notes |
|---------|-------|-------|
| **Slides Count** | 3-20 | Optimal range for presentations |
| **Website URLs** | 10 max | Per request to avoid timeouts |
| **Context Sources** | 10 max | Text-based context sources |
| **Image Generation** | 5 max | To balance quality and speed |
| **Processing Time** | 30-120s | Depends on complexity and context |
| **Prompt Length** | 10-500 chars | Main topic description |

---

## 🎯 Use Cases

### **1. Business Pitches**
```json
{
  "slides_count": 12,
  "prompt": "Series A Funding Pitch for FinTech Startup",
  "industry_sector": "Financial Technology",
  "one_line_pitch": "AI-powered personal finance advisor for Gen Z",
  "problem_solving": "Young adults lack financial literacy and personalized guidance",
  "unique_solution": "Gamified AI advisor that learns spending patterns and provides real-time guidance",
  "target_audience": "18-28 year olds with disposable income",
  "business_model": "Freemium with premium financial planning features",
  "revenue_plan": "Subscription revenue + affiliate partnerships with financial institutions"
}
```

### **2. Academic Presentations**
```json
{
  "slides_count": 15,
  "prompt": "Climate Change Impact on Coastal Cities",
  "website_urls": ["https://en.wikipedia.org/wiki/Sea_level_rise"],
  "context_sources": ["IPCC reports show 1.1°C warming has already caused measurable sea level rise"],
  "tone": "Academic",
  "language": "English",
  "generate_images": true
}
```

### **3. Product Launches**
```json
{
  "slides_count": 8,
  "prompt": "Revolutionary Smart Home Security System",
  "industry_sector": "IoT & Home Security",
  "unique_solution": "AI-powered security that learns family patterns and detects anomalies",
  "target_audience": "Homeowners aged 30-55 with household income >$75k",
  "competitors": "Ring, Nest, SimpliSafe",
  "color_theme": "modern"
}
```

---

## 🚨 Error Handling

### **Common Errors:**
1. **Invalid slides_count**: Must be between 3-20
2. **Empty prompt**: Minimum 10 characters required
3. **Invalid website URLs**: URLs must be accessible
4. **RAG processing errors**: Context sources may fail to process
5. **Image generation failures**: DALL-E API issues

### **Error Response Format:**
```json
{
  "success": false,
  "error": "Detailed error message",
  "slides_count": 8,
  "processing_time": 5.23,
  "generated_images": [],
  "context_sources_used": []
}
```

---

## 🎉 Summary

The **Unified Presentation Generation API** combines:

1. ✅ **AI-Powered Content Generation** (GPT-4o-mini)
2. ✅ **RAG Context Integration** (Website + Text sources)
3. ✅ **Business Information Processing** (Pitch, model, competitors)
4. ✅ **Professional Image Generation** (DALL-E 3)
5. ✅ **Multi-language Support** (Global reach)
6. ✅ **Flexible Theming** (Multiple color themes)
7. ✅ **XML Output Format** (Ready for presentation tools)

This single endpoint replaces the need for multiple API calls and provides a comprehensive presentation generation solution with intelligent context integration!