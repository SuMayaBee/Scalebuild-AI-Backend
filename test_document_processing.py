#!/usr/bin/env python3
"""
Simple test for document processing without API dependencies
"""
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

from Rag.services.document_processor import document_processor

def test_text_processing():
    """Test basic text document processing"""
    print("🧪 Testing Text Document Processing...")
    
    # Sample text content
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
    
    try:
        # Test text processing
        result = document_processor.extract_text_from_file(
            file_content=sample_text.encode('utf-8'),
            filename="test_document.txt"
        )
        
        print(f"✅ Text extracted: {len(result['text'])} characters")
        print(f"✅ Metadata: {result['metadata']}")
        print(f"✅ First 100 chars: {result['text'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Text processing failed: {e}")
        return False

def test_json_processing():
    """Test JSON document processing"""
    print("\n🧪 Testing JSON Document Processing...")
    
    # Sample JSON content
    sample_json = {
        "company": "ScalebuildAI",
        "products": [
            {
                "name": "RAG System",
                "description": "Document-based Q&A system",
                "features": ["Upload documents", "Ask questions", "Get answers"]
            },
            {
                "name": "Video Generation",
                "description": "AI-powered video creation",
                "features": ["Text to video", "Custom prompts", "High quality"]
            }
        ],
        "contact": {
            "email": "info@scalebuild.ai",
            "website": "https://scalebuild.ai"
        }
    }
    
    try:
        import json
        json_bytes = json.dumps(sample_json, indent=2).encode('utf-8')
        
        result = document_processor.extract_text_from_file(
            file_content=json_bytes,
            filename="company_info.json"
        )
        
        print(f"✅ JSON processed: {len(result['text'])} characters")
        print(f"✅ Metadata: {result['metadata']}")
        print(f"✅ First 200 chars: {result['text'][:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ JSON processing failed: {e}")
        return False

def test_supported_formats():
    """Test supported formats listing"""
    print("\n🧪 Testing Supported Formats...")
    
    try:
        formats = document_processor.get_supported_formats()
        print(f"✅ Supported formats: {len(formats)}")
        
        for ext, desc in formats.items():
            print(f"   • {ext}: {desc}")
        
        # Test format checking
        test_files = [
            "document.pdf",
            "spreadsheet.xlsx", 
            "presentation.pptx",
            "data.csv",
            "notes.txt",
            "config.json",
            "readme.md",
            "unsupported.xyz"
        ]
        
        print("\n📋 Format Support Check:")
        for filename in test_files:
            supported = document_processor.is_supported_format(filename)
            status = "✅" if supported else "❌"
            print(f"   {status} {filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Format testing failed: {e}")
        return False

def main():
    """Run document processing tests"""
    print("🚀 Starting Document Processing Tests\n")
    
    tests = [
        test_text_processing,
        test_json_processing,
        test_supported_formats
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print(f"\n🏁 Tests Completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All document processing tests passed!")
    else:
        print("⚠️ Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()