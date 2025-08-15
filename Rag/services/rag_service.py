"""
Main RAG Service - Orchestrates document processing and query answering
"""
import os
import hashlib
import uuid
from typing import List, Dict, Any, Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from Rag.services.vector_service import pinecone_service
from Rag.services.embedding_service import embedding_service
from Rag.services.web_scraper_service import web_scraper_service
from Rag.db_models import RAGDocument, RAGDocumentChunk, RAGChatSession, RAGChatMessage
import time
import json

class RAGService:
    def __init__(self):
        """Initialize RAG service"""
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.chat_model = "gpt-4o-mini"  # Using your existing model
        
        print(f"✅ RAG service initialized with chat model: {self.chat_model}")
    
    async def process_website(
        self,
        user_id: int,
        url: str,
        title: Optional[str] = None,
        verify_ssl: bool = True,
        max_pages: int = 1
    ) -> RAGDocument:
        """
        Process a website: scrape, chunk, embed, and store in vector database
        
        Args:
            user_id: User ID who is processing the website
            url: Website URL to scrape
            title: Optional document title
            verify_ssl: Whether to verify SSL certificates
            max_pages: Maximum number of pages to scrape (1 for single page)
            
        Returns:
            RAGDocument: Created document record
        """
        db: Session = SessionLocal()
        try:
            print(f"🌐 Processing website: {url}")
            
            # Scrape website content
            if max_pages > 1:
                scraped_results = web_scraper_service.scrape_website_with_sitemap(url, max_pages)
            else:
                scraped_results = [web_scraper_service.scrape_single_url(url, verify_ssl)]
            
            if not scraped_results:
                raise ValueError(f"No content could be scraped from {url}")
            
            # Combine all scraped content
            combined_content = ""
            combined_metadata = {
                "source_type": "website",
                "urls": [],
                "scraped_pages": len(scraped_results)
            }
            
            for result in scraped_results:
                combined_content += f"\n\n--- Page: {result['url']} ---\n\n"
                combined_content += result['content']
                combined_metadata["urls"].append(result['url'])
            
            # Create document record
            document = RAGDocument(
                user_id=user_id,
                title=title or f"Website: {url}",
                filename=f"website_{hash(url)}.txt",
                file_path=f"rag_websites/{user_id}/{url}",
                file_size=len(combined_content),
                file_type="website",
                status="processing",
                pinecone_namespace=f"user_{user_id}",
                document_metadata=combined_metadata
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            # Chunk the combined content
            print("🔪 Chunking website content...")
            chunks = embedding_service.chunk_text(
                text=combined_content,
                chunk_size=1000,
                chunk_overlap=200
            )
            
            # Generate embeddings for chunks
            print("🧠 Generating embeddings...")
            chunk_texts = [chunk["content"] for chunk in chunks]
            embeddings = await embedding_service.generate_embeddings_batch(chunk_texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            chunk_records = []
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                # Generate unique vector ID
                vector_id = f"web_{document.id}_chunk_{i}"
                
                # Create content hash for deduplication
                content_hash = hashlib.md5(chunk["content"].encode()).hexdigest()
                
                # Prepare metadata
                chunk_metadata = {
                    "document_id": document.id,
                    "user_id": user_id,
                    "source_url": url,
                    "title": document.title,
                    "chunk_index": i,
                    "content": chunk["content"],
                    "char_count": chunk["char_count"],
                    "token_count": chunk["token_count"],
                    "file_type": "website",
                    "source_type": "website"
                }
                
                vectors.append((vector_id, embedding, chunk_metadata))
                
                # Create chunk record for database
                chunk_record = RAGDocumentChunk(
                    document_id=document.id,
                    chunk_index=i,
                    content=chunk["content"],
                    content_hash=content_hash,
                    pinecone_id=vector_id,
                    chunk_metadata=chunk_metadata
                )
                
                chunk_records.append(chunk_record)
            
            # Store vectors in Pinecone
            print("📊 Storing vectors in Pinecone...")
            pinecone_service.upsert_vectors(
                vectors=vectors,
                namespace=f"user_{user_id}"
            )
            
            # Store chunk records in database
            print("💾 Storing chunks in database...")
            db.add_all(chunk_records)
            
            # Update document status
            document.chunks_count = len(chunks)
            document.status = "completed"
            
            db.commit()
            db.refresh(document)
            
            print(f"✅ Website processed successfully: {len(chunks)} chunks created from {len(scraped_results)} pages")
            return document
            
        except Exception as e:
            # Update document status to failed
            if 'document' in locals():
                document.status = "failed"
                db.commit()
            
            print(f"❌ Error processing website: {e}")
            raise
        finally:
            db.close()

    async def process_document(
        self,
        user_id: int,
        file_content: str,
        filename: str,
        file_type: str,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> RAGDocument:
        """
        Process a document: chunk, embed, and store in vector database
        
        Args:
            user_id: User ID who uploaded the document
            file_content: Text content of the document
            filename: Original filename
            file_type: File type (pdf, txt, docx, etc.)
            title: Optional document title
            metadata: Optional additional metadata
            
        Returns:
            RAGDocument: Created document record
        """
        db: Session = SessionLocal()
        try:
            print(f"📄 Processing document: {filename}")
            
            # Create document record
            document = RAGDocument(
                user_id=user_id,
                title=title or filename,
                filename=filename,
                file_path=f"rag_documents/{user_id}/{filename}",
                file_size=len(file_content),
                file_type=file_type,
                status="processing",
                pinecone_namespace=f"user_{user_id}",
                metadata=metadata or {}
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            # Chunk the document
            print("🔪 Chunking document...")
            chunks = embedding_service.chunk_text(
                text=file_content,
                chunk_size=1000,
                chunk_overlap=200
            )
            
            # Generate embeddings for chunks
            print("🧠 Generating embeddings...")
            chunk_texts = [chunk["content"] for chunk in chunks]
            embeddings = await embedding_service.generate_embeddings_batch(chunk_texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            chunk_records = []
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                # Generate unique vector ID
                vector_id = f"doc_{document.id}_chunk_{i}"
                
                # Create content hash for deduplication
                content_hash = hashlib.md5(chunk["content"].encode()).hexdigest()
                
                # Prepare metadata
                chunk_metadata = {
                    "document_id": document.id,
                    "user_id": user_id,
                    "filename": filename,
                    "title": document.title,
                    "chunk_index": i,
                    "content": chunk["content"],  # Store content in metadata for retrieval
                    "char_count": chunk["char_count"],
                    "token_count": chunk["token_count"],
                    "file_type": file_type
                }
                
                vectors.append((vector_id, embedding, chunk_metadata))
                
                # Create chunk record for database
                chunk_record = RAGDocumentChunk(
                    document_id=document.id,
                    chunk_index=i,
                    content=chunk["content"],
                    content_hash=content_hash,
                    pinecone_id=vector_id,
                    metadata=chunk_metadata
                )
                
                chunk_records.append(chunk_record)
            
            # Store vectors in Pinecone
            print("📊 Storing vectors in Pinecone...")
            pinecone_service.upsert_vectors(
                vectors=vectors,
                namespace=f"user_{user_id}"
            )
            
            # Store chunk records in database
            print("💾 Storing chunks in database...")
            db.add_all(chunk_records)
            
            # Update document status
            document.chunks_count = len(chunks)
            document.status = "completed"
            
            db.commit()
            db.refresh(document)
            
            print(f"✅ Document processed successfully: {len(chunks)} chunks created")
            return document
            
        except Exception as e:
            # Update document status to failed
            if 'document' in locals():
                document.status = "failed"
                db.commit()
            
            print(f"❌ Error processing document: {e}")
            raise
        finally:
            db.close()
    
    async def query_documents(
        self,
        user_id: int,
        query: str,
        max_results: int = 5,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Query documents and generate answer using RAG
        
        Args:
            user_id: User ID for namespace filtering
            query: User's question
            max_results: Maximum number of relevant chunks to retrieve
            session_id: Optional chat session ID
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        start_time = time.time()
        
        try:
            print(f"🔍 Processing RAG query: {query}")
            
            # Generate embedding for query
            query_embedding = await embedding_service.generate_embedding(query)
            
            # Search similar vectors in Pinecone
            search_results = pinecone_service.query_vectors(
                query_embedding=query_embedding,
                top_k=max_results,
                namespace=f"user_{user_id}",
                include_metadata=True
            )
            
            if not search_results.matches:
                return {
                    "query": query,
                    "answer": "I couldn't find any relevant information in your documents to answer this question. Please make sure you have uploaded documents related to your query.",
                    "sources": [],
                    "session_id": session_id or str(uuid.uuid4()),
                    "processing_time": time.time() - start_time,
                    "tokens_used": 0
                }
            
            # Extract relevant chunks
            relevant_chunks = []
            context_texts = []
            
            for match in search_results.matches:
                chunk_data = {
                    "content": match.metadata.get("content", ""),
                    "metadata": {
                        "document_id": match.metadata.get("document_id"),
                        "filename": match.metadata.get("filename"),
                        "title": match.metadata.get("title"),
                        "chunk_index": match.metadata.get("chunk_index"),
                        "score": match.score
                    },
                    "score": match.score
                }
                
                relevant_chunks.append(chunk_data)
                context_texts.append(match.metadata.get("content", ""))
            
            # Generate answer using GPT with context
            print("🤖 Generating answer with GPT...")
            answer = await self._generate_answer_with_context(query, context_texts)
            
            # Count tokens used
            total_context = "\n\n".join(context_texts)
            tokens_used = embedding_service.count_tokens(query + total_context + answer)
            
            # Save to chat history if session_id provided
            if session_id:
                await self._save_chat_message(user_id, session_id, query, answer, relevant_chunks, tokens_used, time.time() - start_time)
            
            processing_time = time.time() - start_time
            
            print(f"✅ RAG query completed in {processing_time:.2f}s")
            
            return {
                "query": query,
                "answer": answer,
                "sources": relevant_chunks,
                "session_id": session_id or str(uuid.uuid4()),
                "processing_time": processing_time,
                "tokens_used": tokens_used
            }
            
        except Exception as e:
            print(f"❌ Error processing RAG query: {e}")
            raise
    
    async def _generate_answer_with_context(self, query: str, context_texts: List[str]) -> str:
        """Generate answer using GPT with retrieved context"""
        try:
            # Combine context
            context = "\n\n".join(context_texts)
            
            # Create prompt
            system_prompt = """You are a helpful AI assistant that answers questions based on the provided context from uploaded documents. 

Instructions:
1. Use ONLY the information provided in the context to answer questions
2. If the context doesn't contain enough information, say so clearly
3. Cite specific parts of the documents when possible
4. Be concise but comprehensive
5. If asked about something not in the context, explain that you can only answer based on the uploaded documents

Context from uploaded documents:
{context}

Please answer the following question based on the context above."""

            messages = [
                {
                    "role": "system",
                    "content": system_prompt.format(context=context)
                },
                {
                    "role": "user", 
                    "content": query
                }
            ]
            
            # Generate response
            response = self.openai_client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content
            
            print(f"✅ Generated answer ({len(answer)} characters)")
            return answer
            
        except Exception as e:
            print(f"❌ Error generating answer: {e}")
            return f"I encountered an error while generating an answer: {str(e)}"
    
    async def _save_chat_message(
        self,
        user_id: int,
        session_id: str,
        query: str,
        answer: str,
        sources: List[Dict[str, Any]],
        tokens_used: int,
        processing_time: float
    ):
        """Save chat message to database"""
        db: Session = SessionLocal()
        try:
            # Get or create chat session
            session = db.query(RAGChatSession).filter(RAGChatSession.session_id == session_id).first()
            
            if not session:
                session = RAGChatSession(
                    session_id=session_id,
                    user_id=user_id,
                    title=query[:50] + "..." if len(query) > 50 else query
                )
                db.add(session)
                db.commit()
                db.refresh(session)
            
            # Save user message
            user_message = RAGChatMessage(
                session_id=session_id,
                role="user",
                content=query,
                tokens_used=0,
                processing_time=0
            )
            
            # Save assistant message
            assistant_message = RAGChatMessage(
                session_id=session_id,
                role="assistant",
                content=answer,
                sources=sources,
                tokens_used=tokens_used,
                processing_time=processing_time
            )
            
            db.add_all([user_message, assistant_message])
            db.commit()
            
            print("✅ Chat messages saved to database")
            
        except Exception as e:
            print(f"❌ Error saving chat message: {e}")
        finally:
            db.close()
    
    async def get_chat_history(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get chat history for a session"""
        db: Session = SessionLocal()
        try:
            session = db.query(RAGChatSession).filter(RAGChatSession.session_id == session_id).first()
            
            if not session:
                return None
            
            messages = db.query(RAGChatMessage).filter(
                RAGChatMessage.session_id == session_id
            ).order_by(RAGChatMessage.created_at).all()
            
            return {
                "session_id": session.session_id,
                "user_id": session.user_id,
                "title": session.title,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "sources": msg.sources,
                        "timestamp": msg.created_at,
                        "tokens_used": msg.tokens_used,
                        "processing_time": msg.processing_time
                    } for msg in messages
                ],
                "created_at": session.created_at,
                "updated_at": session.updated_at
            }
            
        except Exception as e:
            print(f"❌ Error getting chat history: {e}")
            return None
        finally:
            db.close()
    
    async def delete_document(self, document_id: int, user_id: int) -> Dict[str, Any]:
        """Delete document and its vectors from both database and Pinecone"""
        db: Session = SessionLocal()
        try:
            # Get document
            document = db.query(RAGDocument).filter(
                RAGDocument.id == document_id,
                RAGDocument.user_id == user_id
            ).first()
            
            if not document:
                return {"success": False, "message": "Document not found"}
            
            # Get all chunk IDs for Pinecone deletion
            chunks = db.query(RAGDocumentChunk).filter(RAGDocumentChunk.document_id == document_id).all()
            vector_ids = [chunk.pinecone_id for chunk in chunks]
            
            # Delete vectors from Pinecone
            if vector_ids:
                pinecone_service.delete_vectors(
                    vector_ids=vector_ids,
                    namespace=f"user_{user_id}"
                )
            
            # Delete from database (cascades to chunks)
            db.delete(document)
            db.commit()
            
            print(f"✅ Deleted document {document_id} and {len(vector_ids)} vectors")
            
            return {
                "success": True,
                "message": f"Document '{document.title}' deleted successfully",
                "deleted_chunks": len(vector_ids)
            }
            
        except Exception as e:
            db.rollback()
            print(f"❌ Error deleting document: {e}")
            return {"success": False, "message": str(e)}
        finally:
            db.close()
    
    def test_services(self) -> Dict[str, bool]:
        """Test all RAG service connections"""
        results = {
            "openai_embeddings": False,
            "openai_chat": False,
            "pinecone": False,
            "database": False
        }
        
        # Test OpenAI embeddings
        try:
            results["openai_embeddings"] = embedding_service.test_connection()
        except:
            pass
        
        # Test OpenAI chat
        try:
            response = self.openai_client.chat.completions.create(
                model=self.chat_model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            results["openai_chat"] = bool(response.choices[0].message.content)
        except:
            pass
        
        # Test Pinecone
        try:
            stats = pinecone_service.get_index_stats()
            results["pinecone"] = "total_vector_count" in stats
        except:
            pass
        
        # Test Database
        try:
            db: Session = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            results["database"] = True
        except:
            pass
        
        return results

# Global RAG service instance
rag_service = RAGService()