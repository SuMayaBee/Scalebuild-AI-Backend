#!/usr/bin/env python3
"""
Simple RAG system test with real document upload and query
"""
import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from Rag.services.rag_service import rag_service

async def test_rag_workflow():
    """Test complete RAG workflow with a sample document"""
    print("🚀 Testing Complete RAG Workflow\n")
    
    # Check service health first
    print("🔍 Checking service health...")
    health = rag_service.test_services()
    
    print("Service Status:")
    for service, status in health.items():
        emoji = "✅" if status else "❌"
        print(f"  {emoji} {service}: {'OK' if status else 'FAILED'}")
    
    if not all(health.values()):
        print("\n⚠️ Some services are not available. Please check your configuration.")
        return False
    
    print("\n📄 Processing sample document...")
    
    # Sample document content
    sample_document = """
    Python Programming Guide
    
    Python is a high-level, interpreted programming language known for its simplicity and readability.
    It was created by Guido van Rossum and first released in 1991.
    
    Key Features of Python:
    1. Easy to learn and use - Python has a simple syntax that makes it accessible to beginners
    2. Interpreted language - No need to compile code before running
    3. Object-oriented programming - Supports classes, objects, inheritance, and encapsulation
    4. Large standard library - Comes with many built-in modules and functions
    5. Cross-platform compatibility - Runs on Windows, macOS, Linux, and other operating systems
    6. Dynamic typing - Variables don't need explicit type declarations
    
    Popular Use Cases:
    - Web development with frameworks like Django and Flask
    - Data science and machine learning with libraries like pandas, NumPy, and scikit-learn
    - Artificial intelligence and deep learning with TensorFlow and PyTorch
    - Automation and scripting for system administration
    - Desktop application development with tkinter or PyQt
    - Game development with pygame
    
    Python Philosophy:
    The Zen of Python includes principles like:
    - Beautiful is better than ugly
    - Explicit is better than implicit
    - Simple is better than complex
    - Readability counts
    
    Getting Started:
    To start programming in Python, you need to install Python from python.org
    and choose a code editor or IDE like VS Code, PyCharm, or IDLE.
    """
    
    try:
        # Process the document
        document = await rag_service.process_document(
            user_id=999,  # Test user ID
            file_content=sample_document,
            filename="python_guide.txt",
            file_type="txt",
            title="Python Programming Guide"
        )
        
        print(f"✅ Document processed successfully!")
        print(f"   • Document ID: {document.id}")
        print(f"   • Chunks created: {document.chunks_count}")
        print(f"   • Status: {document.status}")
        
        # Test queries
        test_queries = [
            "Who created Python and when?",
            "What are the main features of Python?",
            "What is Python used for?",
            "What is the Zen of Python?"
        ]
        
        print(f"\n🔍 Testing queries...")
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n--- Query {i}: {query} ---")
            
            result = await rag_service.query_documents(
                user_id=999,
                query=query,
                max_results=3
            )
            
            print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
            print(f"🔢 Tokens used: {result['tokens_used']}")
            print(f"📊 Sources found: {len(result['sources'])}")
            print(f"💬 Answer: {result['answer'][:200]}...")
            
            if result['sources']:
                print(f"📚 Top source score: {result['sources'][0]['score']:.3f}")
        
        # Clean up
        print(f"\n🧹 Cleaning up test document...")
        delete_result = await rag_service.delete_document(document.id, user_id=999)
        print(f"✅ {delete_result['message']}")
        
        print(f"\n🎉 RAG workflow test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ RAG workflow test failed: {e}")
        return False

async def main():
    """Run the RAG workflow test"""
    success = await test_rag_workflow()
    
    if success:
        print("\n✨ Your RAG system is fully functional!")
        print("\nNext steps:")
        print("1. Start your FastAPI server: uvicorn app.main:app --reload")
        print("2. Visit http://localhost:8000/docs to see the API documentation")
        print("3. Use the /rag/upload endpoint to upload documents")
        print("4. Use the /rag/query endpoint to ask questions")
    else:
        print("\n⚠️ Please check your configuration and try again.")
        print("Make sure you have:")
        print("- Valid OpenAI API key")
        print("- Valid Pinecone API key")
        print("- Database connection working")

if __name__ == "__main__":
    asyncio.run(main())