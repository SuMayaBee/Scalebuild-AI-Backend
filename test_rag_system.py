#!/usr/bin/env python3
"""
Test script for RAG system
"""
import asyncio
import os
from pathlib import Path
import tempfile

# Add the project root to Python path
import sys
sys.path.append(str(Path(__file__).parent))

from Rag.services.document_processor import document_processor
from Rag.services.embedding_service import embedding_service
from Rag.services.vector_service import pinecone_service
from Rag.services.rag_service import rag_service

async def test_document_processing():
    """Test document processing with sample text"""
    print("🧪 Testing Document Processing...")
    
    # Create a sample text document
    sample_text = """
    This is a test document for the RAG system.
    
    The RAG (Retrieval-Augmented Generation) system combines the power of 
    information retrieval with large language models to provide accurate 
    and contextual responses based on uploaded documents.
    
    Key features:
    1. Document upload and processing
    2. Text chunking and embedding
    3. Vector storage in Pinecone
    4. Semantic search and retrieval
    5. GPT-powered answer generation
    
    This system supports multiple file formats including PDF, DOCX, TXT, 
    CSV, XLSX, PPTX, JSON, and Markdown files.
    """
    
    # Test text processing
    result = document_processor.extract_text_from_file(
        file_content=sample_text.encode('utf-8'),
        filename="test_document.txt"
    )
    
    print(f"✅ Text extracted: {len(result['text'])} characters")
    print(f"✅ Metadata: {result['metadata']}")
    
    return result['text']

async def test_embedding_service():
    """Test embedding generation"""
    print("\n🧪 Testing Embedding Service...")
    
    # Test connection
    if embedding_service.test_connection():
        print("✅ OpenAI embedding service connected")
    else:
        print("❌ OpenAI embedding service connection failed")
        return False
    
    # Test embedding generation
    test_text = "This is a test sentence for embedding generation."
    embedding = await embedding_service.generate_embedding(test_text)
    
    print(f"✅ Generated embedding with {len(embedding)} dimensions")
    
    # Test text chunking
    long_text = "This is a long text. " * 100
    chunks = embedding_service.chunk_text(long_text, chunk_size=200, chunk_overlap=50)
    
    print(f"✅ Text chunked into {len(chunks)} pieces")
    
    return True

async def test_vector_service():
    """Test Pinecone vector operations"""
    print("\n🧪 Testing Vector Service...")
    
    try:
        # Test index stats
        stats = pinecone_service.get_index_stats()
        print(f"✅ Pinecone connected - Total vectors: {stats.get('total_vector_count', 0)}")
        
        # Test vector operations with sample data
        test_embedding = [0.1] * 1536  # Sample embedding
        test_vectors = [
            ("test_vector_1", test_embedding, {"content": "Test content 1", "source": "test"})
        ]
        
        # Upsert test vector
        pinecone_service.upsert_vectors(test_vectors, namespace="test")
        print("✅ Test vector upserted")
        
        # Query test vector
        results = pinecone_service.query_vectors(
            query_embedding=test_embedding,
            top_k=1,
            namespace="test",
            include_metadata=True
        )
        
        if results.matches:
            print(f"✅ Vector query successful - Found {len(results.matches)} matches")
        
        # Clean up test vector
        pinecone_service.delete_vectors(["test_vector_1"], namespace="test")
        print("✅ Test vector cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Pinecone test failed: {e}")
        return False

async def test_full_rag_workflow():
    """Test complete RAG workflow"""
    print("\n🧪 Testing Full RAG Workflow...")
    
    try:
        # Test service health
        health = rag_service.test_services()
        print(f"Service Health: {health}")
        
        if not all(health.values()):
            print("❌ Some services are not healthy, skipping full workflow test")
            return False
        
        # Process a test document
        sample_content = """
        Python is a high-level programming language known for its simplicity and readability.
        It was created by Guido van Rossum and first released in 1991.
        
        Key features of Python:
        - Easy to learn and use
        - Interpreted language
        - Object-oriented programming support
        - Large standard library
        - Cross-platform compatibility
        
        Python is widely used in web development, data science, artificial intelligence,
        automation, and many other fields.
        """
        
        print("📄 Processing test document...")
        document = await rag_service.process_document(
            user_id=1,  # Test user ID
            file_content=sample_content,
            filename="python_guide.txt",
            file_type="txt",
            title="Python Programming Guide"
        )
        
        print(f"✅ Document processed: {document.chunks_count} chunks created")
        
        # Test querying
        print("🔍 Testing document query...")
        query_result = await rag_service.query_documents(
            user_id=1,
            query="What is Python and who created it?",
            max_results=3
        )
        
        print(f"✅ Query processed in {query_result['processing_time']:.2f}s")
        print(f"📝 Answer: {query_result['answer'][:200]}...")
        print(f"📊 Found {len(query_result['sources'])} relevant sources")
        
        # Clean up test document
        delete_result = await rag_service.delete_document(document.id, user_id=1)
        print(f"✅ Cleanup: {delete_result['message']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full RAG workflow test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting RAG System Tests\n")
    
    # Test 1: Document Processing
    try:
        await test_document_processing()
    except Exception as e:
        print(f"❌ Document processing test failed: {e}")
    
    # Test 2: Embedding Service
    try:
        await test_embedding_service()
    except Exception as e:
        print(f"❌ Embedding service test failed: {e}")
    
    # Test 3: Vector Service (only if Pinecone is configured)
    if os.getenv("PINECONE_API_KEY") and os.getenv("PINECONE_API_KEY") != "your_pinecone_api_key_here":
        try:
            await test_vector_service()
        except Exception as e:
            print(f"❌ Vector service test failed: {e}")
    else:
        print("\n⚠️ Skipping Pinecone tests - API key not configured")
    
    # Test 4: Full RAG Workflow (only if all services are available)
    if (os.getenv("OPENAI_API_KEY") and 
        os.getenv("PINECONE_API_KEY") and 
        os.getenv("PINECONE_API_KEY") != "your_pinecone_api_key_here"):
        try:
            await test_full_rag_workflow()
        except Exception as e:
            print(f"❌ Full RAG workflow test failed: {e}")
    else:
        print("\n⚠️ Skipping full workflow test - Services not fully configured")
    
    print("\n🏁 RAG System Tests Completed")

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    asyncio.run(main())