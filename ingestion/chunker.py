#Hybrid Recursive Semantic Chunking 

import uuid
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=75,
    separators=["\n\n", "\n",". ", " ", ""])

def chunk_doc(doc):
    test = doc["text"]
    raw_chunks = text_splitter.split_text(test)
    structured_chunks= []
    
    for index,chunk_text in enumerate(raw_chunks):
        chunk = {
            "chunk_id": str(uuid.uuid4()),
            "document_id": doc["document_id"],
            "filename": doc["filename"],
            "source_type": doc["source_type"],
            "chunk_index": index,
            "text": chunk_text,
        }
        structured_chunks.append(chunk)
    return structured_chunks


#TESTING SCRIPT
if __name__ == "__main__":

    from loader import load_document

    pdf_path = "data/product_docs/sample.pdf"

    document = load_document(pdf_path)

    chunks = chunk_doc(document)

    print(f"\nTOTAL CHUNKS: {len(chunks)}\n")

    for chunk in chunks:

        print("=" * 50)

        print(f"CHUNK INDEX: {chunk['chunk_index']}")

        print(f"CHUNK ID: {chunk['chunk_id']}")

        print(f"SOURCE TYPE: {chunk['source_type']}")

        print("\nTEXT:\n")

        print(chunk["text"])

        print("\n")