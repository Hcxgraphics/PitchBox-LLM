import os
import fitz #pymupdf
import uuid
import re
from docx2pdf import convert



def get_source_type(path):

    normalized_path = path.replace("\\", "/").lower()

    if "product_docs" in normalized_path:
        return "product"

    elif "industry_docs" in normalized_path:
        return "industry"

    return "unknown"



def is_heading(line):  #To indentify is a line
    line = line.strip()
    
    if not line:
        return False
    
    if line.isupper():
        return True
    
    if len(line) <= 5 and line[0].isupper():
        return True
    
    if not re.search(r'[.!?]$', line):
        if len(line.split()) <= 5:
            return True

    return False



def structure_text(text):
    lines = text.split("\n")
    structured_lines = []

    for line in lines:
        if not line: 
            continue
        if is_heading(line):
            structured_lines.append(f"{{H1}}{line.strip()}")
        else:
            structured_lines.append(line.strip())

    return "\n".join(structured_lines)        




def extract_pdf_text(pdf_path):

    pdf = fitz.open(pdf_path)

    all_text = []

    for page in pdf:

        # WORD-LEVEL extraction
        # words = page.get_text("words")
        # page_text = " ".join(word[4] for word in words)

        # BLOCK-LEVEL extraction

        blocks = page.get_text("blocks")
        page_text = ""
        for block in blocks:
            block_text = block[4].strip()
            page_text += block_text + "\n"

        all_text.append(page_text)

    pdf.close()

    final_text = "\n".join(all_text)
    final_text = structure_text(final_text)

    return final_text




def convert_docx_to_pdf(docx_path):

    os.makedirs("temp_pdfs", exist_ok=True)
    filename = os.path.basename(docx_path)

    pdf_filename = filename.replace(".docx", ".pdf")

    output_pdf_path = os.path.join(
        "temp_pdfs",
        pdf_filename
    )


    convert(docx_path, output_pdf_path)

    return output_pdf_path





def load_document(path):

    extension = os.path.splitext(path)[1].lower()

    # ---------------- PDF ----------------

    if extension == ".pdf":

        text = extract_pdf_text(path)

    # ---------------- DOCX ----------------

    elif extension == ".docx":

        pdf_path = convert_docx_to_pdf(path)

        text = extract_pdf_text(pdf_path)

    else:

        raise ValueError(f"Unsupported file type: {extension}")

    # -------------------------------------

    return {
        "document_id": str(uuid.uuid4()),
        "filename": os.path.basename(path),
        "text": text,
        "source_type": get_source_type(path)
    }





# -----------------------------------
# TESTING
# -----------------------------------

if __name__ == "__main__":

    pdf_path = "data/product_docs/sample.pdf"

    docx_path = "data/industry_docs/sample.docx"

    # TEST PDF
    pdf_doc = load_document(pdf_path)

    print("\nPDF LOADED")
    print(pdf_doc["filename"])
    print(pdf_doc["source_type"])
    print(pdf_doc["text"][:1000])

    # TEST DOCX
    docx_doc = load_document(docx_path)

    print("\nDOCX LOADED")
    print(docx_doc["filename"])
    print(docx_doc["source_type"])
    print(docx_doc["text"][:1000])