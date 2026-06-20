import os
import re
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "./data")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
POLICY_FILE = os.path.join(DATA_PATH, "sample_policies.txt")

def chunk_text(text, chunk_size=400, overlap=100):
    """
    Splits text into chunks of roughly chunk_size characters with overlap.
    A simple but robust slide-window text chunker for learning purposes.
    """
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Try to find a sentence boundary or word boundary to cut nicely
        if end < len(text):
            # Look backwards up to 50 chars for a period or space
            last_period = chunk.rfind('.')
            if last_period > chunk_size - 100:
                end = start + last_period + 1
            else:
                last_space = chunk.rfind(' ')
                if last_space > chunk_size - 50:
                    end = start + last_space + 1
            chunk = text[start:end]
            
        chunks.append({
            "text": chunk.strip(),
            "start_char": start,
            "end_char": end
        })
        start += (chunk_size - overlap)
        
    return chunks

def extract_metadata(chunk_text):
    """
    Simple rule-based metadata extractor to find document references.
    """
    ref_match = re.search(r'Document Reference:\s*([A-Z0-9\-]+)', chunk_text, re.IGNORECASE)
    section_match = re.search(r'(SECTION \d+:[^-\n]+)', chunk_text)
    
    metadata = {
        "source": "sample_policies.txt",
        "doc_ref": ref_match.group(1) if ref_match else "GENERAL",
        "section": section_match.group(1).strip() if section_match else "UNKNOWN"
    }
    return metadata

def main():
    print("--- STEP 1: Reading Policy File ---")
    if not os.path.exists(POLICY_FILE):
        print(f"Error: {POLICY_FILE} not found. Please create it first.")
        return

    with open(POLICY_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    print("--- STEP 2: Creating Chunks ---")
    # For testing, we split by double newline first to preserve sectional groupings, 
    # then slide chunk within section.
    sections = content.split("SECTION ")
    all_chunks = []
    
    # Process header
    if sections[0].strip():
        header_chunks = chunk_text(sections[0], chunk_size=300, overlap=50)
        for c in header_chunks:
            c["metadata"] = {"source": "sample_policies.txt", "doc_ref": "HEADER", "section": "HEADER"}
            all_chunks.append(c)
            
    # Process sections
    for sec in sections[1:]:
        sec_text = "SECTION " + sec
        metadata = extract_metadata(sec_text)
        sec_chunks = chunk_text(sec_text, chunk_size=350, overlap=80)
        for c in sec_chunks:
            c["metadata"] = metadata
            all_chunks.append(c)

    print(f"Generated {len(all_chunks)} chunks.")
    for idx, c in enumerate(all_chunks[:3]):
        print(f"\nChunk {idx+1} ({c['metadata']['section']}):")
        print(f"Content: {c['text'][:120]}...")

    print("\n--- STEP 3: Initializing Embedding Model ---")
    # Using small local embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("--- STEP 4: Creating Vector DB and Storing Embeddings ---")
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    # Reset/Get collection
    collection = chroma_client.get_or_create_collection(
        name="company_policies",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Prep inputs for ChromaDB
    ids = []
    documents = []
    embeddings = []
    metadatas = []
    
    for idx, chunk in enumerate(all_chunks):
        chunk_id = f"chunk_{idx}"
        embedding = model.encode(chunk["text"]).tolist()
        
        ids.append(chunk_id)
        documents.append(chunk["text"])
        embeddings.append(embedding)
        metadatas.append(chunk["metadata"])

    # Upsert to Chroma
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Successfully stored {len(ids)} vectors in collection '{collection.name}' at '{CHROMA_DB_PATH}'.")

if __name__ == "__main__":
    main()
