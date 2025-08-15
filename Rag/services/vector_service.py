"""
Pinecone Vector Database Service
"""
import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
from pinecone import Pinecone, ServerlessSpec
import time

class PineconeService:
    def __init__(self):
        """Initialize Pinecone service"""
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.environment = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "scalebuild-rag")
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.api_key)
        
        # Initialize or get index
        self.index = self._get_or_create_index()
        
        print(f"✅ Pinecone service initialized with index: {self.index_name}")
    
    def _get_or_create_index(self):
        """Get existing index or create new one"""
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                print(f"🔧 Creating new Pinecone index: {self.index_name}")
                
                # Create index with serverless spec
                self.pc.create_index(
                    name=self.index_name,
                    dimension=3072,  # Match text-embedding-3-large dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=self.environment
                    )
                )
                
                # Wait for index to be ready
                while not self.pc.describe_index(self.index_name).status['ready']:
                    print("⏳ Waiting for index to be ready...")
                    time.sleep(1)
                
                print(f"✅ Index {self.index_name} created successfully")
            
            return self.pc.Index(self.index_name)
            
        except Exception as e:
            print(f"❌ Error initializing Pinecone index: {e}")
            raise
    
    def upsert_vectors(
        self, 
        vectors: List[Tuple[str, List[float], Dict[str, Any]]], 
        namespace: Optional[str] = None,
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        Upsert vectors to Pinecone in batches to handle large documents
        
        Args:
            vectors: List of (id, embedding, metadata) tuples
            namespace: Optional namespace for organization
            batch_size: Number of vectors per batch (default: 100)
            
        Returns:
            Combined upsert response from Pinecone
        """
        try:
            if not vectors:
                print("⚠️ No vectors to upsert")
                return {"upserted_count": 0}
            
            total_vectors = len(vectors)
            print(f"📊 Upserting {total_vectors} vectors in batches of {batch_size}...")
            
            # Calculate batch size based on estimated payload size
            # Each vector with 3072 dimensions is roughly 12KB + metadata
            # Target ~3MB per batch to stay under 4MB limit
            estimated_size_per_vector = 15000  # ~15KB per vector (conservative estimate)
            max_safe_batch_size = min(batch_size, 200)  # Never exceed 200 vectors per batch
            
            # Adjust batch size if vectors are large
            if total_vectors > 50:
                max_safe_batch_size = min(max_safe_batch_size, 50)
            
            total_upserted = 0
            responses = []
            
            # Process vectors in batches
            for i in range(0, total_vectors, max_safe_batch_size):
                batch_vectors = vectors[i:i + max_safe_batch_size]
                batch_num = (i // max_safe_batch_size) + 1
                total_batches = (total_vectors + max_safe_batch_size - 1) // max_safe_batch_size
                
                print(f"📦 Processing batch {batch_num}/{total_batches} ({len(batch_vectors)} vectors)...")
                
                # Format vectors for Pinecone
                formatted_vectors = [
                    {
                        "id": vector_id,
                        "values": embedding,
                        "metadata": metadata
                    }
                    for vector_id, embedding, metadata in batch_vectors
                ]
                
                # Upsert batch to Pinecone
                try:
                    response = self.index.upsert(
                        vectors=formatted_vectors,
                        namespace=namespace
                    )
                    
                    responses.append(response)
                    total_upserted += len(batch_vectors)
                    
                    print(f"✅ Batch {batch_num}/{total_batches} completed ({len(batch_vectors)} vectors)")
                    
                    # Small delay between batches to avoid rate limiting
                    if batch_num < total_batches:
                        import time
                        time.sleep(0.5)
                        
                except Exception as batch_error:
                    print(f"❌ Error in batch {batch_num}: {batch_error}")
                    # Continue with next batch instead of failing completely
                    continue
            
            print(f"✅ Successfully upserted {total_upserted}/{total_vectors} vectors to Pinecone")
            
            # Return combined response
            return {
                "upserted_count": total_upserted,
                "total_batches": len(responses),
                "failed_batches": total_batches - len(responses)
            }
            
        except Exception as e:
            print(f"❌ Error upserting vectors: {e}")
            raise
    
    def query_vectors(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        namespace: Optional[str] = None,
        filter_metadata: Optional[Dict[str, Any]] = None,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Query similar vectors from Pinecone
        
        Args:
            query_embedding: Query vector embedding
            top_k: Number of results to return
            namespace: Optional namespace to query
            filter_metadata: Optional metadata filter
            include_metadata: Whether to include metadata in response
            
        Returns:
            Query response from Pinecone
        """
        try:
            response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                namespace=namespace,
                filter=filter_metadata,
                include_metadata=include_metadata,
                include_values=False
            )
            
            print(f"✅ Queried Pinecone, found {len(response.matches)} matches")
            return response
            
        except Exception as e:
            print(f"❌ Error querying vectors: {e}")
            raise
    
    def delete_vectors(
        self,
        vector_ids: List[str],
        namespace: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Delete vectors from Pinecone
        
        Args:
            vector_ids: List of vector IDs to delete
            namespace: Optional namespace
            
        Returns:
            Delete response from Pinecone
        """
        try:
            response = self.index.delete(
                ids=vector_ids,
                namespace=namespace
            )
            
            print(f"✅ Deleted {len(vector_ids)} vectors from Pinecone")
            return response
            
        except Exception as e:
            print(f"❌ Error deleting vectors: {e}")
            raise
    
    def delete_namespace(self, namespace: str) -> Dict[str, Any]:
        """
        Delete entire namespace from Pinecone
        
        Args:
            namespace: Namespace to delete
            
        Returns:
            Delete response from Pinecone
        """
        try:
            response = self.index.delete(
                delete_all=True,
                namespace=namespace
            )
            
            print(f"✅ Deleted namespace '{namespace}' from Pinecone")
            return response
            
        except Exception as e:
            print(f"❌ Error deleting namespace: {e}")
            raise
    
    def get_index_stats(self, namespace: Optional[str] = None) -> Dict[str, Any]:
        """
        Get index statistics
        
        Args:
            namespace: Optional namespace to get stats for
            
        Returns:
            Index statistics
        """
        try:
            stats = self.index.describe_index_stats()
            
            if namespace and namespace in stats.namespaces:
                return {
                    "namespace": namespace,
                    "vector_count": stats.namespaces[namespace].vector_count,
                    "total_vector_count": stats.total_vector_count,
                    "dimension": stats.dimension
                }
            
            return {
                "total_vector_count": stats.total_vector_count,
                "dimension": stats.dimension,
                "namespaces": {ns: info.vector_count for ns, info in stats.namespaces.items()}
            }
            
        except Exception as e:
            print(f"❌ Error getting index stats: {e}")
            raise
    
    def generate_vector_id(self, prefix: str = "doc") -> str:
        """Generate unique vector ID"""
        return f"{prefix}_{uuid.uuid4().hex[:12]}"

# Global Pinecone service instance
pinecone_service = PineconeService()