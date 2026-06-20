# Project 1: Enterprise RAG Assistant
*Duration: 4 Weeks | Focus: Retrieval-Augmented Generation*

## 📖 Project Brief
Students will build a local knowledge retrieval system that parses enterprise documentation (PDFs, TXT files) and answers user questions with semantic intelligence, hybrid search (keyword + vector), and accurate source citations. The UI will be built using Streamlit.

---

## 🎯 Learning Objectives
- Master the RAG (Retrieval-Augmented Generation) pipeline architecture.
- Understand tokenization, text-chunking strategies (size and overlap), and vector embedding models.
- Set up and manage a vector database locally (ChromaDB).
- Implement **Hybrid Search** (combining BM25 keyword matching with dense semantic embeddings).
- Formulate dynamic system prompts that force the LLM to cite raw chunks and ground responses to prevent hallucinations.
- Evaluate the RAG system's accuracy and performance.

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
|  [(Local Vector DB)] <============================+                    |
|                                                   ║                    |
|  [User Query] ───────────────────────────+        ║ (Semantic Match)   |
|         │                                │        ║                    |
|         ▼ (BM25 Keyword Search)          ▼        ║                    |
|  [(Keyword Scoring)]                  [(Dense Retrieval)]              |
|         │                                │                             |
|         +───────────────► ◄──────────────+                             |
|                           │                                            |
|                           ▼ (Reciprocal Rank Fusion - RRF)             |
|                  [Top-K Hybrid Chunks]                                 |
|                           │                                            |
|                           ▼ (Format System Prompt context + query)     |
|                  [Gemini API / LLM Wrapper]                            |
|                           │                                            |
|                           ▼ (Synthesis with Source Citation)           |
|                  [Streamlit Conversational UI]                         |
|                                                                        |
+------------------------------------------------------------------------+
```

---

## 🚦 Step-by-Step Implementation Guide

Follow these steps to build and run the Enterprise RAG Assistant:

1. **Environment Setup:** Create a python virtual environment and install dependencies listed in `requirements.txt`.
2. **Configure Environment Variables:** Copy `.env.example` to `.env` and configure paths. If you have a Gemini API key, paste it under `GEMINI_API_KEY`.
3. **Data Inspection:** Examine the raw source document at `data/sample_policies.txt` to identify structural sections.
4. **Implement Text Splitter:** In `src/ingest.py`, build the sliding-window text chunker (`chunk_text`) that splits sections with character size (e.g. 400 chars) and overlap (e.g. 100 chars).
5. **Metadata Extraction:** Build `extract_metadata` in `src/ingest.py` to tag each chunk with section headers and document reference IDs automatically.
6. **Initialize Embeddings:** Initialize the local HuggingFace `SentenceTransformer('all-MiniLM-L6-v2')` model inside `src/ingest.py`.
7. **Database Storage:** Set up the persistent ChromaDB client, generate embeddings for all text chunks, and upsert documents, vectors, and metadata dicts into the database.
8. **Test Ingestion:** Run `python src/ingest.py` and inspect the printouts to verify the local vector index is populated.
9. **Build Keyword Retreival:** In `src/search.py`, tokenize the document corpus and initialize the `BM25Okapi` keyword ranking algorithm.
10. **Build Hybrid Merger:** Implement Reciprocal Rank Fusion (RRF) algorithm inside `HybridRetriever.hybrid_search` in `src/search.py` to merge rankings from ChromaDB search and BM25 search.
11. **Draft Streamlit UI:** Create the conversational front-end in `src/app.py` using Streamlit's chat inputs and session state to display chat histories.
12. **Configure Prompt & Citation:** In the Streamlit app, structure a system instruction that passes the top-K hybrid chunks as context and forces the LLM (Gemini or offline mock fallback) to generate answers citing sources explicitly (e.g., `[Doc 1]`).

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
- Prompt the LLM (using Gemini API or mock/local LLMs) to synthesize answers containing bracketed source citations (e.g., `[Source: document.txt, Chunk 3]`).
- **Deliverable:** Full `src/app.py` Streamlit app running locally.

---

## 📁 Repository Structure
```
P1-enterprise-rag/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── sample_policies.txt
└── src/
    ├── ingest.py
    ├── search.py
    └── app.py
```

---

## 🚀 Setup & Execution

### 1. Install Dependencies
Run the following inside your virtual environment:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Rename `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```
Ensure you add your `GEMINI_API_KEY` to run the active LLM synthesis step. If no key is set, the system will use a local offline simulated fallback.

### 3. Run Ingestion
Ingest the sample policy files:
```bash
python src/ingest.py
```

### 4. Run the Streamlit Interface
Launch the dashboard:
```bash
streamlit run src/app.py
```

---

## 📊 Grading Rubric (100 Points)

| Criteria | Weight | Description |
| :--- | :--- | :--- |
| **Data Ingestion & Chunking** | 20% | Correct use of overlap splitters; handles document indexing correctly without data duplication. |
| **Hybrid Search & Retrieval** | 30% | Working hybrid ranking pipeline combining semantic query and keyword matching. |
| **LLM Output & Citations** | 25% | Responses are correctly grounded to the retrieved documents, containing clear citations. |
| **UI/UX & Code Quality** | 15% | Streamlit app layout is intuitive; Python code has appropriate comments and modular functions. |
| **Advanced Extensions** | 10% | Completion of extension tasks (e.g. metadata filtering or customized splitters). |

---

## 🛠️ Troubleshooting & Tips
- **ChromaDB issues:** If Chroma throws database locks, delete the `chroma_db/` folder to clear indices and re-run `python src/ingest.py`.
- **API Limits:** If Gemini API keys hit rate limits, check the console output to verify fallback simulation is working.
- **Missing packages:** Ensure your virtual environment is active before running commands.
