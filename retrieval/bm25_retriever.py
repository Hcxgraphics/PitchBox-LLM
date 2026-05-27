from rank_bm25 import BM25Okapi  #BM25 stores lexical statistics

def tokenize(text):
    return text.lower().split()


def create_bm25_index(chunks):
    corpus=[]
    for chunk in chunks:
        tokens = tokenize(chunk["text"])
        corpus.append(tokens)
    bm25 = BM25Okapi(corpus)
    return bm25


def bm25_search(query, bm25, chunks, top_k=5):
    query_tokens = tokenize(query)
    scores = bm25.get_scores(query_tokens)

    ranked_indices = sorted(range(len(scores)), key = lambda i: scores[i], reverse = True)
    results = []

    for rank, idx in enumerate(ranked_indices[:top_k]):
        results.append({
            "rank": rank + 1,
            "bm25_score": float(scores[idx]),
            "chunk": chunks[idx]
        })

    return results





#TESTING SCRIPT
if __name__ == "__main__":

    from ingestion.loader import load_document
    from ingestion.chunker import chunk_doc


    path = "data/product_docs/sample.pdf"

    document = load_document(path)

    chunks = chunk_doc(document)

    bm25 = create_bm25_index(chunks)

    query = "Google founders and founding year"

    results = bm25_search(
        query,
        bm25,
        chunks,
        top_k=3
    )

    print("\nBM25 RESULTS\n")

    for result in results:

        print("=" * 60)

        print(f"RANK: {result['rank']}")

        print(f"BM25 SCORE: {result['bm25_score']}")

        print("\nTEXT:\n")

        print(result["chunk"]["text"])

        print("\n")