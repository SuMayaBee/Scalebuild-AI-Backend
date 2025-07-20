from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from openai import OpenAI
import base64
from services.storage_service import upload_to_gcs
import io
import os
import json

# --- OpenAI Models ---
model = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
openai_client = OpenAI()

# --- Predefined Color Palettes ---
COLOR_PALETTES = {
    "Neon Pop": ["#FF0000", "#00FF00", "#D500FF", "#FF00FF", "#F6FF00"],
    "Deep Dusk": ["#112266", "#3A176A", "#782AB6", "#B51FA7", "#F70072"],
    "Sunset Sorbet": ["#FF2350", "#FF5D2A", "#FF9945", "#FFB347", "#FFE156"],
    "Emerald City": ["#016A53", "#019267", "#01B087", "#00C9A7", "#16D5C7"],
    "Coffee Tones": ["#6A4E42", "#7E5C4C", "#9C6D59", "#B08B74", "#CDC1B5"],
    "Purple Parade": ["#5C258D", "#763AA6", "#A25BCF", "#C569E6", "#E159F8"]
}

# --- Logo Styles ---
LOGO_STYLES = [
    "Cartoon Logo",
    "App Logo", 
    "Modern Mascot Logos",
    "Black And White Line Logos",
    "Minimalists and Elegant Logos",
    "Vintage Custom Logos",
    "Modern Sharp Lined Logos"
]

# --- Logo Design Generation ---
logo_design_template = """You are an expert logo designer and brand strategist with extensive experience in creating professional brand identities. Your task is to create a comprehensive logo design specification based on the user's requirements.

Logo Title: {logo_title}
Logo Vision: {logo_vision}
Selected Color Palette: {color_palette_name} - {color_palette_colors}
Logo Style: {logo_style}

Based on the provided information, create a detailed logo design specification that a graphic designer can use to create the actual logo.

Analyze the inputs and create a professional logo design specification in JSON format:

{{
    "logo_overview": {{
        "title": "{logo_title}",
        "concept": "Brief description of the main logo concept",
        "target_audience": "Who this logo is designed for",
        "brand_message": "What message the logo communicates"
    }},
    "design_specifications": {{
        "style_interpretation": "How the selected style will be applied",
        "visual_concept": "Main visual concept based on the vision",
        "composition": "Overall layout and arrangement",
        "proportions": "Size relationships between elements"
    }},
    "color_implementation": {{
        "palette_name": "{color_palette_name}",
        "primary_color": "Main color from the palette with hex code",
        "secondary_color": "Supporting color with hex code", 
        "accent_colors": "Additional colors for highlights",
        "color_psychology": "Why these colors work for this brand"
    }},
    "typography": {{
        "font_style": "Recommended font style for the logo text",
        "font_weight": "Weight and characteristics",
        "text_treatment": "How text should be styled",
        "legibility": "Considerations for readability"
    }},
    "visual_elements": {{
        "main_symbol": "Primary visual element or icon",
        "supporting_elements": "Additional design elements",
        "style_characteristics": "How the chosen style influences the design",
        "symbolism": "Meaning behind the visual elements"
    }},
    "design_variations": {{
        "primary_version": "Main logo layout",
        "horizontal_version": "Horizontal arrangement", 
        "icon_only": "Symbol without text",
        "monochrome": "Single color version"
    }},
    "technical_details": {{
        "scalability": "How the logo works at different sizes",
        "applications": "Where this logo will work best",
        "file_formats": "Recommended formats for different uses",
        "minimum_size": "Smallest usable size"
    }},
    "implementation_notes": {{
        "design_priorities": "Most important design considerations",
        "style_execution": "How to execute the chosen style effectively",
        "brand_alignment": "How the design aligns with the vision"
    }}
}}

Create a professional, actionable logo design specification."""

logo_design_prompt = PromptTemplate.from_template(logo_design_template)
logo_design_chain = logo_design_prompt | model | StrOutputParser()

# --- Logo Description Generation ---
logo_description_template = """You are a creative logo designer. Create a detailed visual description of a logo based on the following requirements:

Logo Title: {logo_title}
Logo Vision: {logo_vision}
Color Palette: {color_palette_name} - {color_palette_colors}
Logo Style: {logo_style}

Generate a comprehensive, visual description of the logo that includes:

**Overall Design Concept:**
- How the logo title and vision translate into visual elements
- The main concept that ties everything together
- The overall aesthetic and feel

**Style Implementation:**
- How the selected "{logo_style}" style is executed
- Specific style characteristics that will be visible
- Visual techniques used to achieve this style

**Color Usage:**
- How the {color_palette_name} palette is applied
- Which colors are used for which elements
- Color combinations and gradients if applicable

**Visual Elements:**
- Primary symbols, icons, or imagery
- Typography treatment and font characteristics
- Layout and composition details
- Size relationships between different elements

**Technical Execution:**
- How the logo vision is visually implemented
- Specific details a designer would need to know
- Professional finishing touches and refinements

Create a detailed description that a skilled designer could use to create the exact logo envisioned. Focus on specific visual details, proportions, and styling that capture the essence of the request."""

logo_description_prompt = PromptTemplate.from_template(logo_description_template)
logo_description_chain = logo_description_prompt | model | StrOutputParser()

# --- Logo Image Generation Template ---
logo_image_template = """
STRICT REQUIREMENTS (MUST FOLLOW):
1. **Only** output the **logo graphic**—no swatches, no color‐chip circles, no labels, no extra icons.
2. Do **NOT** display any representation of the color palette itself.
3. Background must be fully **transparent** (no gradients, no frames, no backgrounds).
4. Center the logo in the canvas; do not add borders or decorative elements.

DESIGN BRIEF:
- Logo Title: {logo_title}
- Style: {logo_style}
- Concept/Vision: {logo_vision}
- **Color Guidance (internal use only):** {color_palette_str}

Use the above HEX codes to pick your fill and stroke colors, but do not render the HEX codes, swatches, or sample circles in the image.
"""



async def generate_logo_design(logo_title: str, logo_vision: str, color_palette_name: str, logo_style: str):
    """Generate a comprehensive logo design specification using GPT-4o"""
    try:
        # Get color palette
        color_palette_colors = COLOR_PALETTES.get(color_palette_name, [])
        color_palette_str = ", ".join(color_palette_colors)
        
        # Generate detailed design specification
        design_spec = ""
        async for chunk in logo_design_chain.astream({
            "logo_title": logo_title,
            "logo_vision": logo_vision,
            "color_palette_name": color_palette_name,
            "color_palette_colors": color_palette_str,
            "logo_style": logo_style
        }):
            design_spec += chunk
        
        # Try to parse as JSON, if it fails, return as text
        try:
            parsed_spec = json.loads(design_spec.strip())
            return {
                "design_specification": parsed_spec,
                "raw_specification": design_spec.strip(),
                "logo_title": logo_title,
                "generation_type": "structured"
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, return as text specification
            return {
                "design_specification": design_spec.strip(),
                "logo_title": logo_title,
                "generation_type": "text"
            }
    except Exception as e:
        print(f"Error in logo design generation: {e}")
        raise e

async def generate_logo_description(logo_title: str, logo_vision: str, color_palette_name: str, logo_style: str):
    """Generate a detailed visual description of the logo using GPT-4o"""
    try:
        # Get color palette
        color_palette_colors = COLOR_PALETTES.get(color_palette_name, [])
        color_palette_str = ", ".join(color_palette_colors)
        
        description = ""
        async for chunk in logo_description_chain.astream({
            "logo_title": logo_title,
            "logo_vision": logo_vision,
            "color_palette_name": color_palette_name,
            "color_palette_colors": color_palette_str,
            "logo_style": logo_style
        }):
            description += chunk
        
        return {
            "logo_description": description.strip(),
            "logo_title": logo_title,
            "parameters": {
                "logo_vision": logo_vision,
                "color_palette": color_palette_name,
                "logo_style": logo_style
            }
        }
    except Exception as e:
        print(f"Error in logo description generation: {e}")
        raise e

async def generate_logo_image(logo_title: str, logo_vision: str, color_palette_name: str, logo_style: str):
    """Generate a logo image using a direct prompt with DALL-E 3, then upload to GCS"""
    try:
        # Get color palette
        color_palette_colors = COLOR_PALETTES.get(color_palette_name, [])
        color_palette_str = ", ".join(color_palette_colors)
        
        # Create the direct prompt
        direct_prompt = logo_image_template.format(
            logo_title=logo_title,
            logo_vision=logo_vision,
            color_palette_str=color_palette_str,
            logo_style=logo_style
        )
        
        # Generate image using DALL-E 3
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=direct_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json"
        )

        if response.data and response.data[0].b64_json:
            image_data = base64.b64decode(response.data[0].b64_json)
            
            # Create filename
            safe_title = "".join(c for c in logo_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            file_name = f"logo_{safe_title.replace(' ', '_')[:30]}.png"
            file_obj = io.BytesIO(image_data)

            bucket_name = os.getenv("GCS_BUCKET_NAME")
            if not bucket_name:
                raise Exception("GCS_BUCKET_NAME environment variable is not set")

            # Upload to Google Cloud Storage
            public_url = upload_to_gcs(file_obj, file_name, "image/png", bucket_name)
            
            return {
                "logo_image_url": public_url,
                "logo_title": logo_title,
                "enhanced_prompt": direct_prompt,
                "image_model": "dall-e-3",
                "original_request": {
                    "logo_title": logo_title,
                    "logo_vision": logo_vision,
                    "color_palette_name": color_palette_name,
                    "logo_style": logo_style
                }
            }
        else:
            raise Exception("Failed to generate logo image or no image data returned.")

    except Exception as e:
        print(f"Error in logo image generation: {e}")
        raise e

async def generate_complete_logo(logo_title: str, logo_vision: str, color_palette_name: str, logo_style: str):
    """Generate both design specification and logo image"""
    try:
        # Generate design specification
        design_result = await generate_logo_design(logo_title, logo_vision, color_palette_name, logo_style)
        
        # Generate logo image
        image_result = await generate_logo_image(logo_title, logo_vision, color_palette_name, logo_style)
        
        # Combine results
        return {
            **design_result,
            "logo_image_url": image_result["logo_image_url"],
            "enhanced_prompt": image_result["enhanced_prompt"],
            "image_model": image_result["image_model"]
        }
        
    except Exception as e:
        print(f"Error in complete logo generation: {e}")
        raise e
