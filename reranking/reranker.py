from sentence_transformers import CrossEncoder


reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_chunks(query, retrieved_chunks):

    pairs = []

    for item in retrieved_chunks:

        chunk_text = item["chunk"]["text"]

        pairs.append(
            [query, chunk_text]
        )


    scores = reranker_model.predict(
        pairs
    )

    reranked_results = []

    for item, score in zip(retrieved_chunks, scores):

        item["rerank_score"] = float(score)

        reranked_results.append(item)

    reranked_results.sort(

        key=lambda x: x["rerank_score"],

        reverse=True
    )

    return reranked_results


#It is slower as every query chunk pair requires full inference -> Expensive & Highly accurate