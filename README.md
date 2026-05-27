RAG Pipeline :

Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
HNSW Retrieval
   ↓
Threshold Filtering
   ↓
 Dynamic Top-K  #Retrieval until similarity quality drops significantly, as some queries need 1 chunk while others need 10
   ↓
Semantic Refinement
   ↓
Cross-Encoder Reranking
   ↓
Hybrid Retrieval
   ↓
Query Expansion
   ↓
Context Compression
   ↓
Self-Improving Retrieval
   ↓
LLM Generation



Using Hybrid search orchestration : 
Query
 ↓
Dense Semantic Retrieval
 +
BM25 Sparse Retrieval
 ↓
Fusion
 ↓
Reranking
 ↓
Final Results

REFERENCES:
https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089 

https://osamadev.medium.com/building-a-full-rag-chatbot-using-python-sentence-transformers-and-chromadb-205dcbc3752c

https://www.pingcap.com/article/mastering-faiss-vector-database-a-beginners-handbook/

https://homayounsrp.medium.com/6-types-of-retrieval-augmented-generation-rag-techniques-you-should-know-b45de9071c79

https://www.pinecone.io/learn/series/rag/rerankers/ : Rankers are slow but retrivers are fast i.e. we use two stages as retrieving a small set of documents from a large dataset is much faster than reranking a large set of documents.