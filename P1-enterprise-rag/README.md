# Project 1: Enterprise RAG Assistant
*Duration: 4 Weeks | Focus: Retrieval-Augmented Generation*

## 📖 Project Brief
Students will build a local knowledge retrieval system that parses enterprise documentation (PDFs, TXT files) and answers user questions with semantic intelligence, hybrid search (keyword + vector), and accurate source citations. The application coordinates tools using the **Google Antigravity SDK (ADK)** and renders a conversational front-end in Streamlit.

---

## 🎯 Learning Objectives
- Master the RAG (Retrieval-Augmented Generation) pipeline architecture.
- Understand tokenization, text-chunking strategies (size and overlap), and vector embedding models.
- Set up and manage a vector database locally (ChromaDB).
- Implement **Hybrid Search** (combining BM25 keyword matching with dense semantic embeddings).
- Configure a **Google Antigravity Agent** and define custom Python search tools.
- Formulate dynamic system prompts that force the Agent to ground answers and cite resources.

---

## 🏗️ Project Architecture Diagram

```
+------------------------------------------------------------------------+
|                      RAG ARCHITECTURE DIAGRAM                          |
+------------------------------------------------------------------------+
|                                                                        |
|  [Raw Documents] (sample_policies.txt)                                 |
|         │                                                              |
|         ▼ (Section Splitting & Character Overlap Chunking)             |
|  [Text Chunks]                                                         |
|         │                                                              |
|         ▼ (HuggingFace sentence-transformers/all-MiniLM-L6-v2)         |
|  [Vector Embeddings]                                                   |
|         │                                                              |
|         ▼ (ChromaDB persistent database write)                         |
|  [(Local Vector DB)] <================================+                |
|                                                       ║                |
|  [User Query]                                         ║ (Tool Call)    |
|         │                                             ║                |
|         ▼ (Inception)                                 ║                |
|  [Antigravity Agent] ──► (Decides to search) ──► [Search Tool]         |
|         │                                             │                |
|         │                                             ▼                |
|         │                                     [Hybrid Search Node]     |
|         │                                       - Vector distance      |
|         │                                       - BM25 text score      |
|         │                                             │                |
|         │◄────────────────────────────────────────────┘                |
|         │  (Returns context documents & citations)                     |
|         ▼                                                              |
|  [Streamlit Chat UI Output]                                            |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to build and run the RAG Agent:

1. **Environment Setup:** Create a python virtual environment and install dependencies listed in `requirements.txt`.
2. **Setup Credentials:** Configure Gemini API keys in the `.env` file.
3. **Data Inspection:** Examine the raw source document at `data/sample_policies.txt` to identify structural sections.
4. **Implement Text Splitter:** In `src/ingest.py`, build the sliding-window text chunker (`chunk_text`) that splits sections with character size (e.g. 400 chars) and overlap (e.g. 100 chars).
5. **Metadata Extraction:** Build `extract_metadata` in `src/ingest.py` to tag each chunk with section headers and document reference IDs automatically.
6. **Initialize Embeddings:** Initialize the local HuggingFace `SentenceTransformer('all-MiniLM-L6-v2')` model inside `src/ingest.py`.
7. **Database Storage:** Set up the persistent ChromaDB client, generate embeddings for all text chunks, and upsert documents, vectors, and metadata dicts into the database.
8. **Test Ingestion:** Run `python src/ingest.py` and inspect the printouts to verify the local vector index is populated.
9. **Build Hybrid Retriever:** In `src/search.py`, implement Reciprocal Rank Fusion (RRF) inside `HybridRetriever.hybrid_search` to merge rankings from ChromaDB semantic search and BM25 token matching.
10. **Define Agent Tool:** In `src/app.py`, define a python tool `search_company_policies(query: str) -> str` containing a descriptive docstring so the model knows when and how to call it.
11. **Configure Antigravity Agent:** Set up the `LocalAgentConfig` in `src/app.py`, registering the search tool and writing clear system instructions.
12. **Build Conversational UI:** Initialize the `Agent` inside an async wrapper and hook it to Streamlit chat inputs to stream outputs.

---

## 📅 Week-by-Week Deliverables

### Week 1: Data Ingestion & Chunking
- Set up project structure, load raw documents.
- Implement text splitters (RecursiveCharacterTextSplitter) and analyze different chunk sizes.
- **Deliverable:** `src/ingest.py` executable script.

### Week 2: Embeddings & Vector Database
- Initialize a local embedding model (HuggingFace `sentence-transformers/all-MiniLM-L6-v2` or similar).
- Generate vector embeddings for text chunks and index them into ChromaDB.
- **Deliverable:** Populated local Chroma database directory.

### Week 3: Hybrid Search Retrieval
- Build a Python retriever class combining ChromaDB semantic querying and BM25 BM25 keyword search.
- Implement Reciprocal Rank Fusion (RRF) to combine rank lists.
- **Deliverable:** `src/search.py` query testing script.

### Week 4: Front-End UI & Prompt engineering
- Implement a Streamlit user interface featuring a chat layout.
- Bind the hybrid search tool to a `google-antigravity` agent config.
- Prompt the Agent to synthesize answers containing bracketed source citations (e.g., `[Doc 1]`).
- **Deliverable:** Full `src/app.py` Streamlit app running locally.

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Data Ingestion & Chunking** | 20% | Correct use of overlap splitters; handles document indexing correctly without data duplication. |
| **Hybrid Search & Retrieval** | 25% | Working hybrid ranking pipeline combining semantic query and keyword matching. |
| **Antigravity Tool Bindings** | 30% | Correct implementation of custom Python search tools with clear docstrings registered on the agent. |
| **LLM Output & Citations** | 15% | Responses are correctly grounded to the retrieved documents, containing clear citations. |
| **UI/UX & Code Quality** | 10% | Streamlit app layout is intuitive; Python code has appropriate comments. |

---

## 🛠️ Troubleshooting & Tips
- **ChromaDB issues:** If Chroma throws database locks, delete the `chroma_db/` folder to clear indices and re-run `python src/ingest.py`.
- **API Limits:** If Gemini API keys hit rate limits, check the console output to verify fallback simulation is working.
