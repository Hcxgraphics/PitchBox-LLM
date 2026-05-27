import numpy as np
import faiss
from reranking.reranker import rerank_chunks

def embed_query(query, embedding_model): #Creating query embeddings
    query_vector = embedding_model.encode([query])
    return np.array(query_vector, dtype="float32")


def retrieve_chunks(
        query, 
        index, 
        chunks, 
        embedding_model , 
        top_k = 5, 
        similarity_threshold = 0.65, 
        dynamic_gap_threshold=0.08
        ):
    
    query_vector = embed_query(query, embedding_model)
    faiss.normalize_L2(query_vector)  # Normalize the query vector for cosine similarity

    # distances, indices = index.search(query_vector, top_k)
    similarities, indices = index.search(query_vector, top_k)

    retrieved_chunks = []
    previous_similarity = None

    for rank, chunk_index in enumerate(indices[0]):
        # distance = distances[0][rank]
        similarity = similarities[0][rank]
        if similarity < similarity_threshold:
            continue  # Skip chunks that do not meet the similarity threshold
        
        if previous_similarity is not None:
            gap = previous_similarity - similarity
            if gap > dynamic_gap_threshold:
                print(f"\n Stopping retrival due to semantic quality drop") # Skip chunks that have a large gap in similarity
                break
        previous_similarity = similarity
        
        chunk_data = chunks[chunk_index]
        retrieved_chunks.append({
            "rank": rank + 1,
            "similarity_score": float(similarity),
            "chunk": chunk_data
        })
        
    return retrieved_chunks




if __name__ == "__main__":

    from ingestion.loader import load_document
    from ingestion.chunker import chunk_doc
    from embeddings.embedder import (embed_chunks, model )
    from vectorStore.faiss import (create_faiss_index)

    path = "data/product_docs/sample.pdf"
    document = load_document(path)
    chunks = chunk_doc(document)

    print(f"\nTOTAL CHUNKS: {len(chunks)}")

    embeddings = embed_chunks(chunks)

    index = create_faiss_index(
        embeddings,
        index_type="hnsw",
        use_gpu=True
    )

    query = "Google was founded by whom and when?"

    results = retrieve_chunks(
        query=query,

        index=index,

        chunks=chunks,

        embedding_model=model,

        top_k=3
    )

    reranked_results = rerank_chunks(
        query, results 
    )

    print("\nRETRIEVAL RESULTS\n")

    for result in reranked_results:

        print("=" * 60)

        print(f"RANK: {result['rank']}")

        print(f"SIMILARITY SCORE: {result['similarity_score']}")

        print(f"RERANK SCORE: {result['rerank_score']}")

        print("\nTEXT:\n")

        print(result["chunk"]["text"])

        print("\n")