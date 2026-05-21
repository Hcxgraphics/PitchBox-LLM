#Responsible for creating FAISS index, embeddings, metadata , vectors and return top chunks

from operator import index
import faiss
import numpy as np

def create_faiss_index(embeddings, index_type = "hnsw", use_gpu = False, hnsw_m = 32, ef_construction = 200 ): # efConstruction is for index quality during creation
        embeddings = np.array(embeddings, dtype= "float32") #Converting to float
        dimension = embeddings.shape[1]

        if index_type == "flat":
            index = faiss.IndexFlatL2(dimension) #L2 distance metric : Simpler, easier to implement. Mathematically exact search

        elif index_type == "hnsw":
            index = faiss.IndexHNSWFlat(dimension, hnsw_m) #HNSW (Hierarchical Navigable Small World) : More complex, faster for large datasets. Approximate search

            index.hnsw.efConstruction = ef_construction #Higher values improve recall but increase indexing time and memory usage
        else:
             raise ValueError("Unsupported index type: {index_type}")
        
        if use_gpu:
            num_gpu = faiss.get_num_gpus()
            if num_gpu == 0:
                 print("No GPU found. Using CPU instead.")
            else:
                 print(f"Using GPU: {num_gpu} available.")
                 
                 res = faiss.StandardGpuResources()
                index = faiss.index_cpu_to_gpu(res,0,index)
            
        index.add(embeddings)
        return index








#TESTING SCRIPT
if __name__ == "__main__":

    from ingestion.loader import load_document
    from ingestion.chunker import chunk_document

    from embeddings.embedder import embed_chunks


    path = "data/product_docs/sample.pdf"

    document = load_document(path)
    chunks = chunk_document(document)

    print(f"\nTOTAL CHUNKS: {len(chunks)}")

    embeddings = embed_chunks(chunks)

    print(f"\nEMBEDDINGS CREATED")

    index = create_faiss_index(
        embeddings=embeddings,

        index_type="hnsw",

        use_gpu=True
    )


    print("\nFAISS INDEX CREATED WITH HNSW")

    print(f"\nTOTAL VECTORS: {index.ntotal}")