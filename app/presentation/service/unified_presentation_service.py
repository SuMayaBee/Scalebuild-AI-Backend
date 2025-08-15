"""
Unified Presentation Service - Combines outline, slides generation with RAG integration
"""
import time
import asyncio
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
import re

# Import RAG services
from Rag.services.rag_service import rag_service
from Rag.services.web_scraper_service import web_scraper_service

# Import presentation services
from app.presentation.service.enhanced_image_service import enhanced_image_service

class UnifiedPresentationService:
    """Service that combines presentation generation with RAG context integration"""
    
    def __init__(self):
        self.model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7, streaming=True)
        self.image_service = enhanced_image_service
        print("✅ Unified Presentation Service initialized")
    
    async def generate_presentation_with_context(
        self,
        user_id: int,
        slides_count: int,
        prompt: str,
        color_theme: str = "default",
        website_urls: List[str] = None,
        context_documents: List[Dict[str, Any]] = None,
        industry_sector: str = None,
        one_line_pitch: str = None,
        problem_solving: str = None,
        unique_solution: str = None,
        target_audience: str = None,
        business_model: str = None,
        revenue_plan: str = None,
        competitors: str = None,
        vision: str = None,
        language: str = "English",
        tone: str = "Professional",
        generate_images: bool = True
    ) -> Dict[str, Any]:
        """
        Generate complete presentation with RAG context integration
        """
        start_time = time.time()
        
        try:
            print(f"🎯 Generating unified presentation: {prompt}")
            
            # Step 1: Gather context from RAG sources
            context_data = await self._gather_rag_context(
                user_id=user_id,
                website_urls=website_urls or [],
                context_documents=context_documents or []
            )
            
            # Step 2: Build comprehensive context
            enhanced_context = self._build_enhanced_context(
                prompt=prompt,
                context_data=context_data,
                industry_sector=industry_sector,
                one_line_pitch=one_line_pitch,
                problem_solving=problem_solving,
                unique_solution=unique_solution,
                target_audience=target_audience,
                business_model=business_model,
                revenue_plan=revenue_plan,
                competitors=competitors,
                vision=vision
            )
            
            # Step 3: Generate presentation outline with context
            outline = await self._generate_contextual_outline(
                enhanced_context=enhanced_context,
                slides_count=slides_count,
                language=language
            )
            
            # Step 4: Generate detailed slides
            presentation_xml = await self._generate_contextual_slides(
                title=prompt,
                outline=outline,
                enhanced_context=enhanced_context,
                language=language,
                tone=tone,
                slides_count=slides_count,
                color_theme=color_theme
            )
            
            # Step 5: Skip image generation (always return empty array)
            generated_images = []
            print("🖼️ Image generation skipped (disabled for performance)")
            
            processing_time = time.time() - start_time
            
            print(f"✅ Unified presentation generated in {processing_time:.2f}s")
            
            return {
                "success": True,
                "presentation_xml": presentation_xml,
                "slides_count": slides_count,
                "processing_time": processing_time,
                "generated_images": generated_images,
                "context_sources_used": context_data["sources_used"],
                "prompt": prompt,
                "theme": color_theme,
                "language": language,
                "tone": tone
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Error generating unified presentation: {e}")
            
            return {
                "success": False,
                "presentation_xml": None,
                "slides_count": slides_count,
                "processing_time": processing_time,
                "generated_images": [],
                "context_sources_used": [],
                "error": str(e),
                "prompt": prompt,
                "theme": color_theme,
                "language": language,
                "tone": tone
            }
    
    async def _gather_rag_context(
        self,
        user_id: int,
        website_urls: List[str],
        context_documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Gather context from RAG sources (websites and uploaded documents)"""
        context_data = {
            "website_content": "",
            "context_content": "",
            "sources_used": []
        }
        
        try:
            # Process website URLs
            if website_urls:
                print(f"🌐 Processing {len(website_urls)} website URLs...")
                
                for url in website_urls:
                    try:
                        # Process website with RAG service
                        document = await rag_service.process_website(
                            user_id=user_id,
                            url=url,
                            title=f"Context from {url}",
                            max_pages=1
                        )
                        
                        # Query the processed website for relevant content
                        query_result = await rag_service.query_documents(
                            user_id=user_id,
                            query="Summarize the main content and key information from this website",
                            max_results=3
                        )
                        
                        if query_result["sources"]:
                            website_summary = query_result["answer"]
                            context_data["website_content"] += f"\n\n--- Content from {url} ---\n{website_summary}"
                            
                            context_data["sources_used"].append({
                                "type": "website",
                                "url": url,
                                "title": document.title,
                                "chunks_count": document.chunks_count,
                                "summary": website_summary[:200] + "..."
                            })
                        
                    except Exception as e:
                        print(f"⚠️ Error processing website {url}: {e}")
                        context_data["sources_used"].append({
                            "type": "website",
                            "url": url,
                            "error": str(e)
                        })
            
            # Process uploaded context documents
            if context_documents:
                print(f"📄 Processing {len(context_documents)} uploaded context documents...")
                
                for i, doc_data in enumerate(context_documents):
                    try:
                        filename = doc_data.get("filename", f"context_document_{i+1}")
                        content = doc_data.get("content", "")
                        metadata = doc_data.get("metadata", {})
                        
                        if not content.strip():
                            print(f"⚠️ Empty content in document: {filename}")
                            continue
                        
                        # Process document with RAG service
                        document = await rag_service.process_document(
                            user_id=user_id,
                            file_content=content,
                            filename=filename,
                            file_type=metadata.get("file_type", "txt"),
                            title=f"Context: {filename}",
                            metadata=metadata
                        )
                        
                        # Query the processed document for relevant content
                        query_result = await rag_service.query_documents(
                            user_id=user_id,
                            query="Summarize the key points and important information from this document",
                            max_results=3
                        )
                        
                        if query_result["sources"]:
                            context_summary = query_result["answer"]
                            context_data["context_content"] += f"\n\n--- Document: {filename} ---\n{context_summary}"
                            
                            context_data["sources_used"].append({
                                "type": "document",
                                "filename": filename,
                                "title": document.title,
                                "chunks_count": document.chunks_count,
                                "file_type": metadata.get("file_type", "txt"),
                                "file_size": len(content),
                                "summary": context_summary[:200] + "..."
                            })
                            
                            print(f"✅ Processed context document: {filename}")
                        
                    except Exception as e:
                        print(f"⚠️ Error processing context document {i+1}: {e}")
                        context_data["sources_used"].append({
                            "type": "document",
                            "filename": doc_data.get("filename", f"document_{i+1}"),
                            "error": str(e)
                        })
            
            return context_data
            
        except Exception as e:
            print(f"❌ Error gathering RAG context: {e}")
            return context_data
    
    def _build_enhanced_context(
        self,
        prompt: str,
        context_data: Dict[str, Any],
        **business_fields
    ) -> str:
        """Build comprehensive context for presentation generation"""
        
        context_parts = [f"Main Topic: {prompt}"]
        
        # Add business context fields
        business_context = []
        field_mapping = {
            "industry_sector": "Industry Sector",
            "one_line_pitch": "One-Line Pitch",
            "problem_solving": "Problem Being Solved",
            "unique_solution": "Unique Solution",
            "target_audience": "Target Audience",
            "business_model": "Business Model",
            "revenue_plan": "Revenue Plan",
            "competitors": "Competitors",
            "vision": "Vision"
        }
        
        for field, label in field_mapping.items():
            value = business_fields.get(field)
            if value:
                business_context.append(f"{label}: {value}")
        
        if business_context:
            context_parts.append("Business Context:\n" + "\n".join(business_context))
        
        # Add RAG context
        if context_data["website_content"]:
            context_parts.append("Website Context:" + context_data["website_content"])
        
        if context_data["context_content"]:
            context_parts.append("Additional Context:" + context_data["context_content"])
        
        return "\n\n".join(context_parts)
    
    async def _generate_contextual_outline(
        self,
        enhanced_context: str,
        slides_count: int,
        language: str
    ) -> List[str]:
        """Generate presentation outline with enhanced context"""
        
        outline_template = """Based on the following comprehensive context, generate a structured presentation outline with exactly {slides_count} main topics.

Context:
{enhanced_context}

Generate exactly {slides_count} slide topics that would make for an engaging and well-structured presentation in {language}.
Each topic should be a clear, concise heading that flows logically from one to another.

Format the response as a simple list of topics, one per line, without numbering or bullet points.
Make sure the topics:
1. Flow logically from introduction to conclusion
2. Cover the key aspects based on the provided context
3. Are clear and engaging for the audience
4. Utilize the business context and external sources provided
5. Are appropriate for a {slides_count}-slide presentation

Example format:
Introduction to [Topic]
Current Market Landscape
Key Challenges and Opportunities
Our Solution Approach
Implementation Strategy
Results and Impact
Future Vision

Generate exactly {slides_count} topics now:"""

        prompt_template = PromptTemplate.from_template(outline_template)
        chain = prompt_template | self.model | StrOutputParser()
        
        try:
            outline_text = ""
            async for chunk in chain.astream({
                "enhanced_context": enhanced_context,
                "slides_count": slides_count,
                "language": language
            }):
                outline_text += chunk
            
            # Parse outline into list
            outline_lines = [line.strip() for line in outline_text.split('\n') if line.strip()]
            
            # Ensure we have exactly the requested number of slides
            if len(outline_lines) > slides_count:
                outline_lines = outline_lines[:slides_count]
            elif len(outline_lines) < slides_count:
                # Pad with generic topics if needed
                while len(outline_lines) < slides_count:
                    outline_lines.append(f"Additional Topic {len(outline_lines) + 1}")
            
            print(f"✅ Generated outline with {len(outline_lines)} topics")
            return outline_lines
            
        except Exception as e:
            print(f"❌ Error generating outline: {e}")
            # Fallback outline
            return [f"Slide {i+1} Topic" for i in range(slides_count)]
    
    async def _generate_contextual_slides(
        self,
        title: str,
        outline: List[str],
        enhanced_context: str,
        language: str,
        tone: str,
        slides_count: int,
        color_theme: str
    ) -> str:
        """Generate detailed slides with enhanced context"""
        
        slides_template = """You are an expert presentation designer. Create an engaging presentation in XML format using the provided context and outline.

## PRESENTATION DETAILS
- Title: {title}
- Language: {language}
- Tone: {tone}
- Total Slides: {slides_count}
- Theme: {color_theme}

## CONTEXT INFORMATION
{enhanced_context}

## OUTLINE TO EXPAND
{outline_formatted}

## CORE REQUIREMENTS
1. FORMAT: Use <SECTION> tags for each slide
2. CONTENT: Expand outline topics using the provided context information
3. VARIETY: Each slide must use a DIFFERENT layout component
4. VISUALS: Include detailed image queries (10+ words) on most slides
5. CONTEXT INTEGRATION: Use information from the provided context throughout

## PRESENTATION STRUCTURE
```xml
<PRESENTATION>
<SECTION layout="left" | "right" | "vertical">
  <!-- Include ONE layout component per slide -->
  <!-- Include detailed image queries where appropriate -->
</SECTION>
<!-- Additional slides -->
</PRESENTATION>
```

## AVAILABLE LAYOUTS
Use different layouts for variety:

1. COLUMNS: For comparisons
```xml
<COLUMNS>
  <DIV><H3>First Concept</H3><P>Description from context</P></DIV>
  <DIV><H3>Second Concept</H3><P>Description from context</P></DIV>
</COLUMNS>
```

2. BULLETS: For key points
```xml
<BULLETS>
  <DIV><H3>Main Point</H3><P>Context-based description</P></DIV>
  <DIV><P>Supporting point with context details</P></DIV>
</BULLETS>
```

3. ICONS: For concepts with symbols
```xml
<ICONS>
  <DIV><ICON query="relevant-icon" /><H3>Concept</H3><P>Context-based description</P></DIV>
</ICONS>
```

4. CYCLE: For processes
```xml
<CYCLE>
  <DIV><H3>Step 1</H3><P>Process description from context</P></DIV>
  <DIV><H3>Step 2</H3><P>Next step description</P></DIV>
</CYCLE>
```

5. ARROWS: For cause-effect
```xml
<ARROWS>
  <DIV><H3>Challenge</H3><P>Problem from context</P></DIV>
  <DIV><H3>Solution</H3><P>Solution from context</P></DIV>
</ARROWS>
```

6. TIMELINE: For chronological progression
```xml
<TIMELINE>
  <DIV><H3>Phase 1</H3><P>Timeline item from context</P></DIV>
  <DIV><H3>Phase 2</H3><P>Next phase description</P></DIV>
</TIMELINE>
```

7. PYRAMID: For hierarchical importance
```xml
<PYRAMID>
  <DIV><H3>Vision</H3><P>Top-level goal from context</P></DIV>
  <DIV><H3>Strategy</H3><P>Strategic approach</P></DIV>
</PYRAMID>
```

8. CHART: For data visualization
```xml
<CHART charttype="vertical-bar">
  <TABLE>
    <TR><TD type="label"><VALUE>Metric 1</VALUE></TD><TD type="data"><VALUE>75</VALUE></TD></TR>
    <TR><TD type="label"><VALUE>Metric 2</VALUE></TD><TD type="data"><VALUE>90</VALUE></TD></TR>
  </TABLE>
</CHART>
```

9. IMAGES: Include relevant images
```xml
<IMG query="detailed specific image description related to the context and slide topic" src="https://storage.googleapis.com/deck123/presentation_images/detailed_specific_image_description_related_to_the_context_and_slide_topic.png" />
```
for example n the <IMG> if the query is `an educational setting in Bangladesh showcasing deep learning applications in art and technology` then the src have to be `https://storage.googleapis.com/deck123/presentation_images/an_educational_setting_in_Bangladesh_showcasing_deep_learning_applications_in_art_and_technology.png`

## CRITICAL RULES
1. Generate exactly {slides_count} slides
2. Use information from the provided context throughout
3. Vary layouts - don't repeat the same layout consecutively
4. Include detailed image queries (10+ words) for visual appeal
5. Make content engaging and relevant to the context provided
6. Use appropriate heading hierarchy (H1, H2, H3)
7. Vary SECTION layout attribute (left/right/vertical)

Create a complete XML presentation now:"""

        prompt_template = PromptTemplate.from_template(slides_template)
        chain = prompt_template | self.model | StrOutputParser()
        
        try:
            presentation_xml = ""
            async for chunk in chain.astream({
                "title": title,
                "language": language,
                "tone": tone,
                "slides_count": slides_count,
                "color_theme": color_theme,
                "enhanced_context": enhanced_context,
                "outline_formatted": "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(outline)])
            }):
                presentation_xml += chunk
            
            print(f"✅ Generated presentation XML ({len(presentation_xml)} characters)")
            return presentation_xml
            
        except Exception as e:
            print(f"❌ Error generating slides: {e}")
            return f"<PRESENTATION><SECTION><H1>Error generating presentation: {str(e)}</H1></SECTION></PRESENTATION>"
    
    async def _generate_slide_images(
        self,
        presentation_xml: str,
        context: str
    ) -> List[Dict[str, Any]]:
        """Generate images for slides based on content"""
        
        generated_images = []
        
        try:
            # Extract image queries from XML
            image_queries = re.findall(r'query="([^"]+)"', presentation_xml)
            
            if not image_queries:
                # Generate some default images based on context
                image_queries = [
                    f"professional business presentation slide about {context[:100]}",
                    f"modern infographic style illustration for business presentation",
                    f"clean corporate design elements for professional slides"
                ]
            
            # Limit to maximum 5 images to avoid excessive generation time
            image_queries = image_queries[:5]
            
            print(f"🖼️ Generating {len(image_queries)} images for slides...")
            
            for i, query in enumerate(image_queries):
                try:
                    # Generate image with DALL-E
                    image_url = await self.image_service.generate_image_dalle3(
                        prompt=query,
                        size="1792x1024",  # Landscape format for slides
                        filename=f"slide_image_{i+1}_{int(time.time())}.png"
                    )
                    
                    generated_images.append({
                        "query": query,
                        "url": image_url,
                        "model": "dall-e-3",
                        "size": "1792x1024",
                        "slide_index": i + 1
                    })
                    
                    print(f"✅ Generated image {i+1}/{len(image_queries)}")
                    
                    # Small delay to avoid rate limiting
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"⚠️ Error generating image {i+1}: {e}")
                    generated_images.append({
                        "query": query,
                        "url": None,
                        "error": str(e),
                        "slide_index": i + 1
                    })
            
            return generated_images
            
        except Exception as e:
            print(f"❌ Error in image generation process: {e}")
            return []

# Global service instance
unified_presentation_service = UnifiedPresentationService()