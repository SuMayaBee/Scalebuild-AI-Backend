# 🎬 Gemini Video Generation Setup Guide

This guide explains how to run Google's Gemini AI for video concept generation and production planning.

## 📋 Prerequisites

1. **Google AI Studio Account** with Gemini API access
2. **Gemini API Key** 
3. **Python Environment** with required packages

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
# Navigate to the video directory
cd video

# Install video-specific requirements
pip install -r requirements_video.txt

# Or install individually
pip install google-generativeai python-dotenv
```

### 2. Environment Configuration

Add your Gemini API key to your `.env` file:

```env
# Gemini API Configuration
GOOGLE_API_KEY=your_gemini_api_key_here
# OR alternatively:
GEMINI_API_KEY=your_gemini_api_key_here
```

**How to get your Gemini API key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

### 3. Create Output Directory

```bash
mkdir -p video/generated
```

## 🚀 How to Run

### Option 1: Interactive Script (Recommended)

```bash
# From the project root directory
python video/improved_gemini_video.py
```

This will show you a menu with options:
1. Generate video concept analysis
2. Generate detailed video script
3. Generate concept variations
4. Generate video production plan
5. Custom video concept analysis
6. Exit

### Option 2: Original Simple Script

```bash
# From the project root directory
python video/gemini_video.py
```

This runs the original script with a predefined prompt.

### Option 3: Direct Python Usage

```python
from video.improved_gemini_video import GeminiVideoGenerator

# Initialize generator
generator = GeminiVideoGenerator()

# Generate video concept analysis
analysis = generator.analyze_video_concept(
    "A beautiful sunset over the ocean with waves gently crashing on the shore"
)

# Generate detailed script
script = generator.generate_video_script(
    "A beautiful sunset over the ocean with waves gently crashing on the shore"
)

print(f"Analysis: {analysis}")
print(f"Script: {script}")
```

## 📝 Example Prompts

Here are some example prompts that work well with Veo 3.0:

### 🎭 Dialogue/Character Scenes
```
"A close up of two people staring at a cryptic drawing on a wall, torchlight flickering. A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"
```

### 🌅 Nature Scenes
```
"A serene mountain lake at sunrise with mist rising from the water, birds flying overhead, and gentle ripples on the surface reflecting the golden sky."
```

### 🏙️ Urban Scenes
```
"A bustling city street at night with neon lights reflecting on wet pavement, people walking with umbrellas, and cars passing by with their headlights creating light trails."
```

### 🎨 Abstract/Artistic
```
"Colorful paint drops falling into clear water in slow motion, creating beautiful swirling patterns and mixing colors in an artistic display."
```

## ⏱️ Generation Times

- **Simple scenes**: 2-5 minutes
- **Complex scenes**: 5-15 minutes
- **High-detail scenes**: 10-30 minutes

## 📁 Output

Generated videos are saved to:
- `video/generated/` directory
- Format: MP4
- Typical duration: 5-10 seconds
- Resolution: 1280x720 (HD)

## 🔍 Troubleshooting

### Common Issues:

1. **Authentication Error**
   ```
   Error: Could not load credentials
   ```
   **Solution**: Check that all VEO_* environment variables are set correctly

2. **API Access Error**
   ```
   Error: Permission denied
   ```
   **Solution**: Ensure your service account has Veo 3.0 API access

3. **Timeout Error**
   ```
   Error: Generation timeout
   ```
   **Solution**: Try a simpler prompt or increase max_wait_time

4. **Import Error**
   ```
   ModuleNotFoundError: No module named 'google.genai'
   ```
   **Solution**: Install requirements: `pip install google-genai`

### Debug Mode:

Add debug logging to see more details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 💡 Tips for Better Results

1. **Be Specific**: Detailed prompts work better than vague ones
2. **Include Motion**: Describe movement, camera angles, lighting
3. **Set Scene**: Mention time of day, weather, environment
4. **Character Actions**: Describe what people are doing, saying
5. **Visual Details**: Colors, textures, atmosphere

## 🚨 Rate Limits

- **Concurrent Generations**: Max 2-3 at once
- **Daily Limit**: Check your Google Cloud quota
- **Wait Time**: 30 seconds between generations recommended

## 📊 Monitoring Usage

Check your Google Cloud Console for:
- API usage statistics
- Billing information
- Error logs
- Quota limits

## 🔗 Useful Links

- [Veo 3.0 Documentation](https://cloud.google.com/vertex-ai/generative-ai/docs/video/overview)
- [Google GenAI Python SDK](https://github.com/google/generative-ai-python)
- [Service Account Setup](https://cloud.google.com/iam/docs/service-accounts)