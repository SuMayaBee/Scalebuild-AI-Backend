"""
OpenAI Embedding Service for RAG
"""
import os
from typing import List, Dict, Any
from openai import OpenAI
import tiktoken

class EmbeddingService:
    def __init__(self):
        """Initialize OpenAI embedding service"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "text-embedding-3-large"  # Match Pinecone configuration
        self.max_tokens = 8191  # Max tokens for embedding model
        self.target_dimension = 3072  # Match Pinecone index dimension
        
        # Initialize tokenizer for token counting
        self.tokenizer = tiktoken.encoding_for_model("text-embedding-3-large")
        
        print(f"✅ Embedding service initialized with model: {self.model}")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def truncate_text(self, text: str, max_tokens: int = None) -> str:
        """Truncate text to fit within token limit"""
        if max_tokens is None:
            max_tokens = self.max_tokens
        
        tokens = self.tokenizer.encode(text)
        
        if len(tokens) <= max_tokens:
            return text
        
        # Truncate tokens and decode back to text
        truncated_tokens = tokens[:max_tokens]
        return self.tokenizer.decode(truncated_tokens)
    
    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            # Truncate text if too long
            truncated_text = self.truncate_text(text)
            
            # Generate embedding
            response = self.client.embeddings.create(
                model=self.model,
                input=truncated_text
            )
            
            embedding = response.data[0].embedding
            
            print(f"✅ Generated embedding for text ({len(truncated_text)} chars, {self.count_tokens(truncated_text)} tokens) - {len(embedding)} dimensions")
            return embedding
            
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            raise
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        try:
            # Truncate all texts
            truncated_texts = [self.truncate_text(text) for text in texts]
            
            # Generate embeddings in batch
            response = self.client.embeddings.create(
                model=self.model,
                input=truncated_texts
            )
            
            embeddings = [data.embedding for data in response.data]
            
            total_tokens = sum(self.count_tokens(text) for text in truncated_texts)
            print(f"✅ Generated {len(embeddings)} embeddings in batch ({total_tokens} total tokens) - {len(embeddings[0])} dimensions each")
            
            return embeddings
            
        except Exception as e:
            print(f"❌ Error generating batch embeddings: {e}")
            raise
    
    def chunk_text(
        self, 
        text: str, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200,
        preserve_sentences: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Split text into chunks for embedding
        
        Args:
            text: Text to chunk
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
            preserve_sentences: Try to preserve sentence boundaries
            
        Returns:
            List of chunk dictionaries with content and metadata
        """
        try:
            chunks = []
            
            if preserve_sentences:
                # Split by sentences first
                sentences = text.split('. ')
                current_chunk = ""
                chunk_index = 0
                
                for sentence in sentences:
                    # Add sentence to current chunk
                    test_chunk = current_chunk + sentence + ". "
                    
                    if len(test_chunk) > chunk_size and current_chunk:
                        # Save current chunk and start new one
                        chunks.append({
                            "content": current_chunk.strip(),
                            "chunk_index": chunk_index,
                            "char_count": len(current_chunk),
                            "token_count": self.count_tokens(current_chunk)
                        })
                        
                        # Start new chunk with overlap
                        overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                        current_chunk = overlap_text + sentence + ". "
                        chunk_index += 1
                    else:
                        current_chunk = test_chunk
                
                # Add final chunk
                if current_chunk.strip():
                    chunks.append({
                        "content": current_chunk.strip(),
                        "chunk_index": chunk_index,
                        "char_count": len(current_chunk),
                        "token_count": self.count_tokens(current_chunk)
                    })
            
            else:
                # Simple character-based chunking
                for i in range(0, len(text), chunk_size - chunk_overlap):
                    chunk_text = text[i:i + chunk_size]
                    
                    chunks.append({
                        "content": chunk_text,
                        "chunk_index": len(chunks),
                        "char_count": len(chunk_text),
                        "token_count": self.count_tokens(chunk_text)
                    })
            
            print(f"✅ Split text into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            print(f"❌ Error chunking text: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            # Simple test embedding
            response = self.client.embeddings.create(
                model=self.model,
                input="test connection"
            )
            
            if response.data and len(response.data[0].embedding) == 3072:
                print("✅ OpenAI embedding service connection successful")
                return True
            else:
                print(f"❌ OpenAI embedding service test failed - expected 3072 dimensions, got {len(response.data[0].embedding) if response.data else 0}")
                return False
                
        except Exception as e:
            print(f"❌ OpenAI embedding service connection failed: {e}")
            return False

# Global embedding service instance
embedding_service = EmbeddingService()