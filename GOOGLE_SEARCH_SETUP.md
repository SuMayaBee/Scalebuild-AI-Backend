# Google Search API Setup for Fast Image Search

This guide helps you set up Google Custom Search API for fast image retrieval as an alternative to AI image generation.

## 🚀 Quick Setup

### 1. Get Google Search API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Custom Search API**
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > API Key**
6. Copy your API key

### 2. Create Custom Search Engine

1. Go to [Google Custom Search Engine](https://cse.google.com/cse/)
2. Click **Add** to create a new search engine
3. In **Sites to search**, enter: `*` (to search the entire web)
4. Give it a name like "Presentation Images"
5. Click **Create**
6. Copy your **Search Engine ID** (cx parameter)

### 3. Configure Search Engine for Images

1. In your Custom Search Engine dashboard
2. Click **Setup** tab
3. Turn ON **Image search**
4. Turn ON **SafeSearch**
5. In **Advanced** tab, set:
   - **Image search**: ON
   - **Image size**: Large
   - **Image type**: Photo
   - **Usage rights**: Labeled for reuse

### 4. Add to Environment Variables

Add these to your `.env` file:

```env
# Google Search API Configuration
GOOGLE_SEARCH_API_KEY=your_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
```

## 🧪 Test Your Setup

Run the test script to verify everything works:

```bash
source venv/bin/activate
python test_fast_image_search.py
```

## 📊 API Limits & Pricing

### Free Tier
- **100 queries per day** for free
- Perfect for development and testing

### Paid Tier
- **$5 per 1,000 queries** after free tier
- Much cheaper than DALL-E for high volume

## 🎯 Usage in Your Application

### Fast Image Search (Recommended for speed)
```bash
curl -X POST "http://localhost:8000/presentation/search-image" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "modern office building", "size": "1024x1024"}'
```

### Batch Image Search (For multiple images)
```bash
curl -X POST "http://localhost:8000/presentation/search-images-batch" \
  -H "Content-Type: application/json" \
  -d '["office building", "team meeting", "data chart"]'
```

### AI Generation (Fallback for custom images)
```bash
curl -X POST "http://localhost:8000/presentation/generate-image" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "futuristic office building", "size": "1024x1024"}'
```

## 🔧 Service Health Check

Check which services are available:

```bash
curl "http://localhost:8000/presentation/image-services/health"
```

## ⚡ Performance Comparison

| Service | Speed | Cost | Customization | Quality |
|---------|-------|------|---------------|---------|
| Google Search | ⚡⚡⚡ Fast (1-3s) | 💰 Low | ⭐⭐ Limited | ⭐⭐⭐ Good |
| DALL-E 3 | ⚡ Slow (10-30s) | 💰💰💰 High | ⭐⭐⭐⭐⭐ Full | ⭐⭐⭐⭐⭐ Excellent |

## 🎯 Recommended Strategy

1. **Default**: Use Google Search for speed and cost-effectiveness
2. **Fallback**: Use DALL-E for custom/branded content
3. **Batch**: Use batch processing for multiple images
4. **Cache**: Store frequently used images in your GCS bucket

## 🔍 Search Query Optimization

The service automatically optimizes search queries by:
- Removing special characters
- Adding quality keywords
- Limiting query length
- Filtering for appropriate content

## 🛡️ Content Safety

- SafeSearch is enabled by default
- Usage rights filtering for legal compliance
- Professional image filtering
- Inappropriate content blocking

## 📈 Scaling Considerations

- **Development**: Free tier (100/day) is sufficient
- **Production**: Consider paid tier for higher volume
- **Caching**: Implement image caching to reduce API calls
- **CDN**: Use CDN for faster image delivery

## 🔧 Troubleshooting

### Common Issues:

1. **"API key not configured"**
   - Check your `.env` file has `GOOGLE_SEARCH_API_KEY`

2. **"Search engine ID not found"**
   - Verify `GOOGLE_SEARCH_ENGINE_ID` in `.env`

3. **"No images found"**
   - Try simpler, more common search terms
   - Check if Custom Search Engine is configured for images

4. **"Quota exceeded"**
   - You've hit the daily limit (100 free queries)
   - Consider upgrading to paid tier

### Debug Mode:
Check the FastAPI logs for detailed error messages and search results.