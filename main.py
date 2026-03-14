import pymupdf
from pathlib import Path
from dotenv import load_dotenv
import chromadb
import sys
from anthropic import Anthropic
load_dotenv()

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

def add_chunks_to_collection(collection, file_name, chunks, verbose = False):
    
    if verbose:
        print(f"Putting text extracted from s{file_name} into database")
    existing = collection.get(where={"source":file_name})
    if len(existing["ids"]) > 0:
        if verbose:
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

#peek_at_collection(collection)

results = collection.query(query_texts=["best places to have a nice coffee, cafes, best coffee"],
                           n_results=10)
# Build context with source labels
context_parts = []
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    context_parts.append(f"[Source : {meta['source']}]\n{doc}")

context = "\n\n".join(context_parts)

prompt = f"""Based on the following excerpts from multiple travel guides, answer the question. Reference where the information came from.

Context:
{context}

Question: {sys.argv[1]}
"""
#print(prompt)

client = Anthropic()

response = client.messages.create(model="claude-haiku-4-5-20251001",
                                  max_tokens=1024,
                                  messages = [{"role":"user", "content":prompt}]
                                  )

print(response.content[0].text)