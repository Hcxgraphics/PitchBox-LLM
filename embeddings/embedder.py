from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    texts = []
    for chunk in chunks:
        texts.append(chunk['text'])
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings




#Testing script
if __name__ == "__main__":

    from ingestion.loader import load_document
    from ingestion.chunker import chunk_doc

    path = "data/product_docs/sample.pdf"

    document = load_document(path)

    chunks = chunk_doc(document)

    vectors = embed_chunks(chunks)

    print("\nTOTAL EMBEDDINGS:")
    print(len(vectors))

    print("\nVECTOR DIMENSION:")
    print(len(vectors[0]))

    print("\nFIRST VECTOR:")
    print(vectors[0][:10])