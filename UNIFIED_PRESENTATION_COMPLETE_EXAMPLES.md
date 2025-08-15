# 🎯 Complete Unified Presentation API Examples

## 📋 **All Use Cases with Request & Response Examples**

**Endpoint:** `POST /presentation/generate-unified`  
**Content-Type:** `multipart/form-data`  
**Authentication:** ❌ **NOT REQUIRED**

---

## 1. 🚀 **Minimal Request (Required Fields Only)**

### **Request:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=5" \
  -F "prompt=Introduction to Artificial Intelligence"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"left\">\n<H1>Introduction to Artificial Intelligence</H1>\n<BULLETS>\n<DIV><H3>What is AI?</H3><P>Artificial Intelligence represents the simulation of human intelligence in machines</P></DIV>\n<DIV><P>AI systems can learn, reason, and make decisions</P></DIV>\n</BULLETS>\n<IMG query=\"futuristic AI brain with neural networks and digital connections in blue tones\" src=\"https://storage.googleapis.com/deck123/presentation_images/ai_brain_neural_networks.png\" />\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Types of AI</H2>\n<COLUMNS>\n<DIV><H3>Narrow AI</H3><P>Specialized systems designed for specific tasks</P></DIV>\n<DIV><H3>General AI</H3><P>Hypothetical AI with human-level intelligence</P></DIV>\n</COLUMNS>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 5,
  "processing_time": 23.45,
  "generated_images": [
    {
      "query": "futuristic AI brain with neural networks and digital connections in blue tones",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345678.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    }
  ],
  "context_sources_used": [],
  "prompt": "Introduction to Artificial Intelligence",
  "theme": "default",
  "language": "English",
  "tone": "Professional"
}
```

---

## 2. 🏢 **Business Pitch (Full Business Context)**

### **Request:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=12" \
  -F "prompt=Series A Funding Pitch for HealthTech Startup" \
  -F "color_theme=corporate" \
  -F "industry_sector=Healthcare Technology" \
  -F "one_line_pitch=AI-powered diagnostic platform that reduces misdiagnosis by 40%" \
  -F "problem_solving=Medical misdiagnosis affects 12 million Americans annually, leading to delayed treatment and increased healthcare costs" \
  -F "unique_solution=Our proprietary AI analyzes medical images, lab results, and patient history to provide accurate diagnostic recommendations in real-time" \
  -F "target_audience=Hospitals, diagnostic centers, and healthcare providers with 100+ beds" \
  -F "business_model=SaaS subscription model with per-diagnosis pricing for smaller practices" \
  -F "revenue_plan=Targeting $50M ARR by year 4 through enterprise contracts and API licensing" \
  -F "competitors=IBM Watson Health, Google Health AI, and traditional diagnostic software providers" \
  -F "vision=To eliminate preventable medical errors and make accurate diagnosis accessible to every patient worldwide" \
  -F "language=English" \
  -F "tone=Professional" \
  -F "generate_images=true"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"vertical\">\n<H1>HealthTech AI: Revolutionizing Medical Diagnosis</H1>\n<BULLETS>\n<DIV><H3>The Problem</H3><P>12 million Americans face misdiagnosis annually</P></DIV>\n<DIV><P>Delayed treatment increases healthcare costs by $750B</P></DIV>\n<DIV><P>Current diagnostic tools lack AI-powered accuracy</P></DIV>\n</BULLETS>\n<IMG query=\"modern hospital emergency room with doctors using AI diagnostic tools and digital displays\" src=\"https://storage.googleapis.com/deck123/presentation_images/hospital_ai_diagnosis.png\" />\n</SECTION>\n<SECTION layout=\"left\">\n<H2>Our Solution</H2>\n<ARROWS>\n<DIV><H3>AI Analysis</H3><P>Proprietary algorithms analyze medical images and lab results</P></DIV>\n<DIV><H3>Real-time Recommendations</H3><P>Instant diagnostic suggestions with 95% accuracy</P></DIV>\n<DIV><H3>Reduced Errors</H3><P>40% reduction in misdiagnosis rates</P></DIV>\n</ARROWS>\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Market Opportunity</H2>\n<CHART charttype=\"vertical-bar\">\n<TABLE>\n<TR><TD type=\"label\"><VALUE>Current Market</VALUE></TD><TD type=\"data\"><VALUE>45</VALUE></TD></TR>\n<TR><TD type=\"label\"><VALUE>Projected 2028</VALUE></TD><TD type=\"data\"><VALUE>120</VALUE></TD></TR>\n<TR><TD type=\"label\"><VALUE>Our Target</VALUE></TD><TD type=\"data\"><VALUE>15</VALUE></TD></TR>\n</TABLE>\n</CHART>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 12,
  "processing_time": 67.89,
  "generated_images": [
    {
      "query": "modern hospital emergency room with doctors using AI diagnostic tools and digital displays",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345678.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    },
    {
      "query": "futuristic medical AI interface showing diagnostic analysis and patient data visualization",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_2_1642345679.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 2
    }
  ],
  "context_sources_used": [],
  "prompt": "Series A Funding Pitch for HealthTech Startup",
  "theme": "corporate",
  "language": "English",
  "tone": "Professional"
}
```
---

## 
3. 🌐 **With Website Context Integration**

### **Request:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=10" \
  -F "prompt=Sustainable Energy Solutions for Smart Cities" \
  -F "color_theme=modern" \
  -F "website_urls=https://en.wikipedia.org/wiki/Smart_city,https://en.wikipedia.org/wiki/Renewable_energy" \
  -F "industry_sector=Clean Energy & Smart Infrastructure" \
  -F "target_audience=City planners, government officials, and infrastructure investors" \
  -F "business_model=B2B2C model partnering with municipalities to deploy smart energy grids" \
  -F "language=English" \
  -F "tone=Professional" \
  -F "generate_images=true"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"left\">\n<H1>Smart Cities: The Future of Sustainable Energy</H1>\n<BULLETS>\n<DIV><H3>Urban Energy Challenge</H3><P>Cities consume 78% of global energy and produce 70% of CO2 emissions</P></DIV>\n<DIV><P>Smart city technologies can reduce energy consumption by 30%</P></DIV>\n<DIV><P>Integration of renewable sources is critical for sustainability</P></DIV>\n</BULLETS>\n<IMG query=\"futuristic smart city skyline with solar panels wind turbines and green energy infrastructure at sunset\" src=\"https://storage.googleapis.com/deck123/presentation_images/smart_city_renewable.png\" />\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Smart Energy Solutions</H2>\n<CYCLE>\n<DIV><H3>Generation</H3><P>Distributed renewable energy sources integrated into city infrastructure</P></DIV>\n<DIV><H3>Storage</H3><P>Advanced battery systems and grid-scale energy storage solutions</P></DIV>\n<DIV><H3>Distribution</H3><P>Smart grids with AI-powered load balancing and demand response</P></DIV>\n<DIV><H3>Consumption</H3><P>IoT-enabled buildings with automated energy optimization</P></DIV>\n</CYCLE>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 10,
  "processing_time": 89.23,
  "generated_images": [
    {
      "query": "futuristic smart city skyline with solar panels wind turbines and green energy infrastructure at sunset",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345680.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    }
  ],
  "context_sources_used": [
    {
      "type": "website",
      "url": "https://en.wikipedia.org/wiki/Smart_city",
      "title": "Website: https://en.wikipedia.org/wiki/Smart_city",
      "chunks_count": 8,
      "summary": "Smart cities use IoT sensors, data analytics, and sustainable infrastructure to optimize resource usage and improve quality of life for residents..."
    },
    {
      "type": "website", 
      "url": "https://en.wikipedia.org/wiki/Renewable_energy",
      "title": "Website: https://en.wikipedia.org/wiki/Renewable_energy",
      "chunks_count": 12,
      "summary": "Renewable energy sources including solar, wind, and hydroelectric power are becoming increasingly cost-effective and essential for climate goals..."
    }
  ],
  "prompt": "Sustainable Energy Solutions for Smart Cities",
  "theme": "modern",
  "language": "English",
  "tone": "Professional"
}
```

---

## 4. 📄 **With Document Upload (File Context)**

### **Request (with test files):**

First create test files:
```bash
# Create business plan document
echo "AI Startup Business Plan

Executive Summary:
Our company develops emotional AI technology that enables machines to understand and respond to human emotions. This addresses the $56B emotional AI market opportunity.

Market Analysis:
- Total Addressable Market: $56B by 2028
- Current solutions lack emotional intelligence
- 78% of users prefer emotionally aware AI
- Healthcare, education, and customer service are key verticals

Technology:
- Proprietary emotion recognition algorithms
- Real-time voice, text, and facial analysis
- 95% accuracy in emotion detection
- API-first architecture for easy integration

Business Model:
- API-as-a-Service with usage-based pricing
- Enterprise licensing for large deployments
- Custom development services

Financial Projections:
Year 1: $500K ARR
Year 2: $2.5M ARR
Year 3: $8M ARR
Year 4: $20M ARR

Funding: Seeking $5M Series A" > business_plan.txt

# Create market research
echo "Market Research Report

Survey Results (n=1,500):
- 89% believe current AI feels robotic
- 72% want AI that detects frustration
- 65% would pay premium for emotional AI
- 84% trust AI more when it shows empathy

Competitive Landscape:
- Affectiva: $34M funding, automotive focus
- Beyond Verbal: Voice emotion, acquired 2019
- Emotient: Facial recognition, acquired by Apple
- Realeyes: Attention measurement, $12M funding

Market Trends:
- 156% growth in emotional AI investments
- Healthcare adoption increasing 45% annually
- Customer service automation driving demand
- Regulatory focus on ethical AI development" > market_research.txt
```

Then make the request:
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=15" \
  -F "prompt=Series A Funding Pitch for Emotional AI Startup" \
  -F "color_theme=corporate" \
  -F "industry_sector=Artificial Intelligence" \
  -F "one_line_pitch=Revolutionary AI that understands and responds to human emotions in real-time" \
  -F "problem_solving=Current AI systems lack emotional intelligence, creating poor user experiences and limiting adoption" \
  -F "unique_solution=Proprietary emotional recognition algorithms that detect and respond to human emotions through voice, text, and facial analysis" \
  -F "target_audience=Enterprise customers, app developers, and healthcare providers" \
  -F "business_model=API-as-a-Service with usage-based pricing and enterprise licensing" \
  -F "revenue_plan=Targeting $20M ARR by Year 4 through API subscriptions and enterprise deals" \
  -F "competitors=Affectiva, Beyond Verbal, and traditional AI providers without emotional capabilities" \
  -F "vision=To make AI more human by giving it the ability to understand and respond to emotions" \
  -F "website_urls=https://en.wikipedia.org/wiki/Affective_computing" \
  -F "context_files=@business_plan.txt" \
  -F "context_files=@market_research.txt" \
  -F "language=English" \
  -F "tone=Professional" \
  -F "generate_images=true"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"vertical\">\n<H1>Emotional AI: The Future of Human-Machine Interaction</H1>\n<BULLETS>\n<DIV><H3>The Opportunity</H3><P>$56B emotional AI market by 2028</P></DIV>\n<DIV><P>89% of users find current AI robotic and impersonal</P></DIV>\n<DIV><P>Healthcare, education, and customer service demand emotional intelligence</P></DIV>\n</BULLETS>\n<IMG query=\"futuristic AI interface showing emotional recognition with human faces displaying various emotions and digital analysis\" src=\"https://storage.googleapis.com/deck123/presentation_images/emotional_ai_interface.png\" />\n</SECTION>\n<SECTION layout=\"left\">\n<H2>Market Validation</H2>\n<CHART charttype=\"vertical-bar\">\n<TABLE>\n<TR><TD type=\"label\"><VALUE>Want Emotional AI</VALUE></TD><TD type=\"data\"><VALUE>89</VALUE></TD></TR>\n<TR><TD type=\"label\"><VALUE>Would Pay Premium</VALUE></TD><TD type=\"data\"><VALUE>65</VALUE></TD></TR>\n<TR><TD type=\"label\"><VALUE>Trust Empathetic AI</VALUE></TD><TD type=\"data\"><VALUE>84</VALUE></TD></TR>\n</TABLE>\n</CHART>\n<P>Survey of 1,500 users shows strong demand for emotionally intelligent AI systems</P>\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Our Solution</H2>\n<ARROWS>\n<DIV><H3>Voice Analysis</H3><P>Real-time emotion detection from speech patterns and tone</P></DIV>\n<DIV><H3>Text Understanding</H3><P>Sentiment and emotional context analysis from written communication</P></DIV>\n<DIV><H3>Facial Recognition</H3><P>Computer vision algorithms that identify emotional expressions</P></DIV>\n<DIV><H3>Intelligent Response</H3><P>AI that adapts behavior based on detected emotional state</P></DIV>\n</ARROWS>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 15,
  "processing_time": 134.56,
  "generated_images": [
    {
      "query": "futuristic AI interface showing emotional recognition with human faces displaying various emotions and digital analysis",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345681.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    },
    {
      "query": "modern tech startup office with diverse team working on AI emotion recognition software and data visualizations",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_2_1642345682.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 2
    }
  ],
  "context_sources_used": [
    {
      "type": "website",
      "url": "https://en.wikipedia.org/wiki/Affective_computing",
      "title": "Website: https://en.wikipedia.org/wiki/Affective_computing",
      "chunks_count": 6,
      "summary": "Affective computing is the study and development of systems that can recognize, interpret, process, and simulate human affects..."
    },
    {
      "type": "document",
      "filename": "business_plan.txt",
      "title": "Context: business_plan.txt",
      "chunks_count": 4,
      "file_type": "txt",
      "file_size": 1247,
      "summary": "Business plan outlines emotional AI startup strategy targeting $56B market with proprietary algorithms for voice, text, and facial emotion recognition..."
    },
    {
      "type": "document",
      "filename": "market_research.txt", 
      "title": "Context: market_research.txt",
      "chunks_count": 3,
      "file_type": "txt",
      "file_size": 892,
      "summary": "Market research shows 89% of users find current AI robotic, 65% would pay premium for emotional AI, with strong growth in healthcare adoption..."
    }
  ],
  "prompt": "Series A Funding Pitch for Emotional AI Startup",
  "theme": "corporate",
  "language": "English",
  "tone": "Professional"
}
```---


## 5. 🎓 **Academic Research Presentation**

### **Request:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=12" \
  -F "prompt=Machine Learning Applications in Climate Change Prediction" \
  -F "color_theme=minimal" \
  -F "industry_sector=Environmental Science & AI" \
  -F "website_urls=https://en.wikipedia.org/wiki/Climate_change,https://en.wikipedia.org/wiki/Machine_learning" \
  -F "language=English" \
  -F "tone=Academic" \
  -F "generate_images=true"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"left\">\n<H1>Machine Learning in Climate Science: Predictive Modeling for Environmental Change</H1>\n<BULLETS>\n<DIV><H3>Research Objective</H3><P>Develop ML models to improve climate prediction accuracy and timeline</P></DIV>\n<DIV><P>Address limitations of traditional climate modeling approaches</P></DIV>\n<DIV><P>Integrate multiple data sources for comprehensive analysis</P></DIV>\n</BULLETS>\n<IMG query=\"scientific visualization of climate data with machine learning algorithms analyzing global temperature patterns and weather systems\" src=\"https://storage.googleapis.com/deck123/presentation_images/climate_ml_analysis.png\" />\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Methodology</H2>\n<TIMELINE>\n<DIV><H3>Data Collection</H3><P>Satellite imagery, weather station data, and oceanographic measurements from 1980-2023</P></DIV>\n<DIV><H3>Feature Engineering</H3><P>Temperature gradients, precipitation patterns, and atmospheric pressure variables</P></DIV>\n<DIV><H3>Model Training</H3><P>Deep neural networks and ensemble methods for pattern recognition</P></DIV>\n<DIV><H3>Validation</H3><P>Cross-validation with historical data and comparison to existing models</P></DIV>\n</TIMELINE>\n</SECTION>\n<SECTION layout=\"vertical\">\n<H2>Results and Findings</H2>\n<CHART charttype=\"vertical-bar\">\n<TABLE>\n<TR><TD type=\"label\"><VALUE>Traditional Models</VALUE></TD><TD type=\"data\"><VALUE>72</VALUE></TD></TR>\n<TR><TD type=\"label\"><VALUE>ML Enhanced</VALUE></TD><TD type=\"data\"><VALUE>89</VALUE></TD></TR>\n<TR><TD type=\"label\"><VALUE>Deep Learning</VALUE></TD><TD type=\"data\"><VALUE>94</VALUE></TD></TR>\n</TABLE>\n</CHART>\n<P>Prediction accuracy comparison shows significant improvement with machine learning approaches</P>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 12,
  "processing_time": 78.34,
  "generated_images": [
    {
      "query": "scientific visualization of climate data with machine learning algorithms analyzing global temperature patterns and weather systems",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345683.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    }
  ],
  "context_sources_used": [
    {
      "type": "website",
      "url": "https://en.wikipedia.org/wiki/Climate_change",
      "title": "Website: https://en.wikipedia.org/wiki/Climate_change",
      "chunks_count": 15,
      "summary": "Climate change refers to long-term shifts in global temperatures and weather patterns, primarily caused by human activities since the mid-20th century..."
    },
    {
      "type": "website",
      "url": "https://en.wikipedia.org/wiki/Machine_learning",
      "title": "Website: https://en.wikipedia.org/wiki/Machine_learning",
      "chunks_count": 10,
      "summary": "Machine learning is a method of data analysis that automates analytical model building using algorithms that iteratively learn from data..."
    }
  ],
  "prompt": "Machine Learning Applications in Climate Change Prediction",
  "theme": "minimal",
  "language": "English",
  "tone": "Academic"
}
```

---

## 6. 🌍 **Multi-language Presentation (Spanish)**

### **Request:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=8" \
  -F "prompt=Inteligencia Artificial en la Medicina Moderna" \
  -F "color_theme=modern" \
  -F "industry_sector=Tecnología Médica" \
  -F "one_line_pitch=IA revolucionaria que mejora el diagnóstico médico en un 40%" \
  -F "target_audience=Hospitales y centros médicos en América Latina" \
  -F "language=Spanish" \
  -F "tone=Professional" \
  -F "generate_images=true"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"left\">\n<H1>Inteligencia Artificial en la Medicina Moderna</H1>\n<BULLETS>\n<DIV><H3>Revolución Médica</H3><P>La IA está transformando el diagnóstico y tratamiento médico</P></DIV>\n<DIV><P>Mejora la precisión diagnóstica en un 40%</P></DIV>\n<DIV><P>Reduce los tiempos de análisis de horas a minutos</P></DIV>\n</BULLETS>\n<IMG query=\"hospital moderno con médicos latinos usando tecnología de inteligencia artificial para diagnóstico médico\" src=\"https://storage.googleapis.com/deck123/presentation_images/hospital_ia_latino.png\" />\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Aplicaciones Principales</H2>\n<ICONS>\n<DIV><ICON query=\"stethoscope\" /><H3>Diagnóstico</H3><P>Análisis automatizado de imágenes médicas y síntomas</P></DIV>\n<DIV><ICON query=\"pill\" /><H3>Tratamiento</H3><P>Recomendaciones personalizadas basadas en datos del paciente</P></DIV>\n<DIV><ICON query=\"chart\" /><H3>Monitoreo</H3><P>Seguimiento continuo de signos vitales y progreso</P></DIV>\n</ICONS>\n</SECTION>\n<SECTION layout=\"vertical\">\n<H2>Beneficios para Hospitales</H2>\n<ARROWS>\n<DIV><H3>Eficiencia</H3><P>Reducción del 30% en tiempo de diagnóstico</P></DIV>\n<DIV><H3>Precisión</H3><P>Disminución de errores médicos en un 25%</P></DIV>\n<DIV><H3>Costos</H3><P>Ahorro promedio de $50,000 anuales por hospital</P></DIV>\n</ARROWS>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 8,
  "processing_time": 45.67,
  "generated_images": [
    {
      "query": "hospital moderno con médicos latinos usando tecnología de inteligencia artificial para diagnóstico médico",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345684.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    }
  ],
  "context_sources_used": [],
  "prompt": "Inteligencia Artificial en la Medicina Moderna",
  "theme": "modern",
  "language": "Spanish",
  "tone": "Professional"
}
```

---

## 7. 🚀 **Product Launch Presentation**

### **Request:**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=10" \
  -F "prompt=Revolutionary Smart Home Security System Launch" \
  -F "color_theme=modern" \
  -F "industry_sector=IoT & Home Security" \
  -F "unique_solution=AI-powered security system that learns family patterns and detects anomalies automatically" \
  -F "target_audience=Homeowners aged 30-55 with household income above $75,000" \
  -F "competitors=Ring, Nest, SimpliSafe, and traditional security companies" \
  -F "business_model=Hardware sales with monthly subscription for AI monitoring services" \
  -F "vision=Making home security intelligent and proactive rather than reactive" \
  -F "language=English" \
  -F "tone=Professional" \
  -F "generate_images=true"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"vertical\">\n<H1>SecureAI: The Future of Smart Home Security</H1>\n<BULLETS>\n<DIV><H3>Beyond Traditional Security</H3><P>Move from reactive alarms to proactive AI protection</P></DIV>\n<DIV><P>Learn family patterns and detect unusual behavior</P></DIV>\n<DIV><P>Reduce false alarms by 85% through intelligent analysis</P></DIV>\n</BULLETS>\n<IMG query=\"modern smart home exterior with AI security cameras and sensors integrated seamlessly into architecture at dusk\" src=\"https://storage.googleapis.com/deck123/presentation_images/smart_home_security.png\" />\n</SECTION>\n<SECTION layout=\"left\">\n<H2>Target Market</H2>\n<PYRAMID>\n<DIV><H3>Primary</H3><P>Homeowners 30-55, income $75K+, tech-savvy families</P></DIV>\n<DIV><H3>Secondary</H3><P>Vacation home owners and rental property managers</P></DIV>\n<DIV><H3>Future</H3><P>Commercial properties and small business owners</P></DIV>\n</PYRAMID>\n</SECTION>\n<SECTION layout=\"right\">\n<H2>Competitive Advantage</H2>\n<COLUMNS>\n<DIV><H3>Traditional Systems</H3><P>Ring, Nest: Basic motion detection, high false alarms</P></DIV>\n<DIV><H3>SecureAI</H3><P>Pattern learning, behavioral analysis, 85% fewer false alarms</P></DIV>\n</COLUMNS>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 10,
  "processing_time": 56.78,
  "generated_images": [
    {
      "query": "modern smart home exterior with AI security cameras and sensors integrated seamlessly into architecture at dusk",
      "url": "https://storage.googleapis.com/deck123/presentation_images/slide_image_1_1642345685.png",
      "model": "dall-e-3",
      "size": "1792x1024",
      "slide_index": 1
    }
  ],
  "context_sources_used": [],
  "prompt": "Revolutionary Smart Home Security System Launch",
  "theme": "modern",
  "language": "English",
  "tone": "Professional"
}
```

---

## 8. ❌ **Error Response Example**

### **Request (Invalid slides_count):**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=25" \
  -F "prompt=Test Presentation"
```

### **Response:**
```json
{
  "success": false,
  "presentation_xml": null,
  "slides_count": 25,
  "processing_time": 0.12,
  "generated_images": [],
  "context_sources_used": [],
  "error": "slides_count must be between 3 and 20",
  "prompt": "Test Presentation",
  "theme": "default",
  "language": "English",
  "tone": "Professional"
}
```

---

## 9. ⚠️ **Partial Success (File Processing Error)**

### **Request (with invalid file):**
```bash
curl -X POST "http://localhost:8000/presentation/generate-unified" \
  -F "slides_count=8" \
  -F "prompt=Business Analysis Presentation" \
  -F "context_files=@invalid_file.xyz"
```

### **Response:**
```json
{
  "success": true,
  "presentation_xml": "<PRESENTATION>\n<SECTION layout=\"left\">\n<H1>Business Analysis Presentation</H1>\n<BULLETS>\n<DIV><H3>Analysis Overview</H3><P>Comprehensive business performance evaluation</P></DIV>\n<DIV><P>Key metrics and performance indicators</P></DIV>\n</BULLETS>\n</SECTION>\n</PRESENTATION>",
  "slides_count": 8,
  "processing_time": 34.56,
  "generated_images": [],
  "context_sources_used": [
    {
      "type": "document",
      "filename": "invalid_file.xyz",
      "error": "Unsupported file format"
    }
  ],
  "prompt": "Business Analysis Presentation",
  "theme": "default",
  "language": "English",
  "tone": "Professional"
}
```

---

## 📊 **Response Field Explanations**

### **Success Response Fields:**
- `success`: Boolean indicating if generation was successful
- `presentation_xml`: Complete XML presentation content
- `slides_count`: Number of slides generated
- `processing_time`: Time taken in seconds
- `generated_images`: Array of AI-generated images with URLs
- `context_sources_used`: Array of processed context sources
- `prompt`: Original presentation topic
- `theme`: Color theme used
- `language`: Presentation language
- `tone`: Presentation tone

### **Image Object Fields:**
- `query`: DALL-E prompt used for generation
- `url`: Public URL to generated image
- `model`: AI model used (dall-e-3)
- `size`: Image dimensions (1792x1024)
- `slide_index`: Which slide the image belongs to

### **Context Source Fields:**
- `type`: "website" or "document"
- `url`/`filename`: Source identifier
- `title`: Processed document title
- `chunks_count`: Number of text chunks created
- `file_type`: Document type (for files)
- `file_size`: File size in bytes (for files)
- `summary`: Brief summary of content
- `error`: Error message if processing failed

---

## 🎯 **Key Features Demonstrated:**

1. ✅ **No Authentication Required** - All examples work without tokens
2. ✅ **Multiple File Upload Support** - PDF, DOCX, TXT, CSV, etc.
3. ✅ **Website Context Integration** - Automatic web scraping and processing
4. ✅ **Business Context Processing** - Comprehensive business information
5. ✅ **AI Image Generation** - DALL-E 3 with contextual prompts
6. ✅ **Multi-language Support** - Any language presentations
7. ✅ **Error Handling** - Detailed error responses and partial success
8. ✅ **Rich XML Output** - Professional presentation layouts

The API provides comprehensive presentation generation with intelligent context integration! 🚀