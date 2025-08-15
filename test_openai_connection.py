#!/usr/bin/env python3
"""
Test OpenAI connection with your API key
"""
import sys
from pathlib import Path
import asyncio

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from Rag.services.embedding_service import embedding_service

async def test_openai_embedding():
    """Test OpenAI embedding service"""
    print("🧪 Testing OpenAI Embedding Service...")
    
    try:
        # Test connection
        if embedding_service.test_connection():
            print("✅ OpenAI embedding service connected successfully")
        else:
            print("❌ OpenAI embedding service connection failed")
            return False
        
        # Test embedding generation
        test_text = "This is a test sentence for embedding generation."
        print(f"📝 Generating embedding for: '{test_text}'")
        
        embedding = await embedding_service.generate_embedding(test_text)
        
        print(f"✅ Generated embedding with {len(embedding)} dimensions")
        print(f"✅ First 5 values: {embedding[:5]}")
        
        # Test text chunking
        long_text = """
        This is a longer text that will be chunked into smaller pieces.
        The RAG system uses text chunking to break down large documents
        into manageable pieces that can be embedded and searched effectively.
        
        Each chunk should contain enough context to be meaningful on its own,
        while also having some overlap with adjacent chunks to maintain
        continuity of information.
        
        This approach allows for more precise retrieval of relevant information
        when users ask questions about the uploaded documents.
        """
        
        print(f"\n📄 Testing text chunking...")
        chunks = embedding_service.chunk_text(
            text=long_text, 
            chunk_size=200, 
            chunk_overlap=50
        )
        
        print(f"✅ Text chunked into {len(chunks)} pieces")
        for i, chunk in enumerate(chunks):
            print(f"   Chunk {i+1}: {chunk['char_count']} chars, {chunk['token_count']} tokens")
            print(f"   Content: {chunk['content'][:100]}...")
        
        # Test batch embedding generation
        print(f"\n🔄 Testing batch embedding generation...")
        chunk_texts = [chunk['content'] for chunk in chunks]
        embeddings = await embedding_service.generate_embeddings_batch(chunk_texts)
        
        print(f"✅ Generated {len(embeddings)} embeddings in batch")
        print(f"✅ Each embedding has {len(embeddings[0])} dimensions")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

async def main():
    """Run OpenAI tests"""
    print("🚀 Starting OpenAI Connection Tests\n")
    
    success = await test_openai_embedding()
    
    if success:
        print("\n🎉 All OpenAI tests passed! Your API key is working correctly.")
        print("\n📋 Next steps:")
        print("1. Set up your Pinecone API key in .env file")
        print("2. Run the full RAG system test")
        print("3. Start uploading documents and asking questions!")
    else:
        print("\n❌ OpenAI tests failed. Please check:")
        print("1. Your OPENAI_API_KEY in the .env file")
        print("2. Your OpenAI account has sufficient credits")
        print("3. Your API key has the correct permissions")

if __name__ == "__main__":
    asyncio.run(main())