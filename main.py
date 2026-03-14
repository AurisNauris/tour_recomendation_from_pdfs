import pymupdf
from pathlib import Path
from dotenv import load_dotenv
import chromadb
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

def add_chunks_to_collection(collection, file_name, chunks):
    
    print(f"Putting text extracted from s{file_name} into database")
    existing = collection.get(where={"source":file_name})
    if len(existing["ids"]) > 0:
        print(f"Skipping {file_name}, already in database")
        return
    
    ids = [f"{file_name}_{i}" for i in range(len(chunks))]
    collection.add(ids=ids,
                documents=chunks,
                metadatas=[{"source":file_name} for _ in chunks])
    
def peek_at_collection(collection):
    print("Total items: ", collection.count())
    # peek at a few entries
    sample = collection.peek()
    for i in range(min(3, len(sample["ids"]))):
        print(f"ID: {sample['ids'][i]}")
        print(f"Source: {sample['metadatas'][i]['source']}")
        print(f"Text: {sample['documents'][i][:100]}...")


guide_dir = Path("guides")
pdf_file_paths = list(guide_dir.glob("*.pdf"))
file_names = [fp.stem for fp in pdf_file_paths]
pdf_extracted = [extract_text_from_pdf(pdf_path) for pdf_path in pdf_file_paths]
chunked_text = [simple_chunking(source) for source in pdf_extracted]

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="travel_guides")

for file_name, chunks in zip(file_names, chunked_text):
    add_chunks_to_collection(collection, file_name, chunks)

peek_at_collection(collection)
