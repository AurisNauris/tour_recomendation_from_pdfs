import pymupdf
from pathlib import Path
from dotenv import load_dotenv

#load_dotenv()

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return " ".join(pages)

def simple_chunking(text):

    chunks = []
    for i in range(0, len(text), 400):
        chunk = text[i:i+500]
        chunks.append(chunk)
    
    if len(chunks[-1]) != 500:
        chunks[-1] = text[-500:]
    
    return chunks


guide_dir = Path("guides")
pdf_file_paths = list(guide_dir.glob("*.pdf"))

pdf_extracted = [extract_text_from_pdf(pdf_path) for pdf_path in pdf_file_paths[2:]]
chunked_text = [simple_chunking(source) for source in pdf_extracted]
print(len(chunked_text))