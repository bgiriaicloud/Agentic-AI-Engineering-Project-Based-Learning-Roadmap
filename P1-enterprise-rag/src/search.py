import os
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

class HybridRetriever:
    def __init__(self):
        # Load local embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load vector database
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = self.chroma_client.get_collection(name="company_policies")
        
        # Fetch all documents to initialize BM25
        all_docs = self.collection.get()
        self.doc_ids = all_docs["ids"]
        self.documents = all_docs["documents"]
        self.metadatas = all_docs["metadatas"]
        
        # Tokenize documents for BM25
        tokenized_corpus = [doc.lower().split(" ") for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def keyword_search(self, query, top_k=5):
        """
        Retrieves documents matching query based on BM25.
        """
        tokenized_query = query.lower().split(" ")
        scores = self.bm25.get_scores(tokenized_query)
        
        # Zip and sort documents by score
        ranked_docs = sorted(
            zip(self.doc_ids, self.documents, self.metadatas, scores),
            key=lambda x: x[3],
            reverse=True
        )
        return ranked_docs[:top_k]

    def vector_search(self, query, top_k=5):
        """
        Retrieves documents based on semantic cosine similarity from ChromaDB.
        """
        query_embedding = self.model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format matching output format of keyword_search
        formatted_results = []
        if results["ids"]:
            for idx in range(len(results["ids"][0])):
                formatted_results.append((
                    results["ids"][0][idx],
                    results["documents"][0][idx],
                    results["metadatas"][0][idx],
                    1 - results["distances"][0][idx] # Convert distance to similarity score
                ))
        return formatted_results

    def hybrid_search(self, query, top_k=3, rr_constant=60):
        """
        Merges keyword search and vector search results using Reciprocal Rank Fusion (RRF).
        RRF Score formula: RRF_Score = sum( 1 / (rr_constant + rank) )
        """
        keyword_results = self.keyword_search(query, top_k=10)
        vector_results = self.vector_search(query, top_k=10)
        
        rrf_scores = {}
        doc_details = {}
        
        # Apply RRF rankings to keyword results
        for rank, (doc_id, doc_text, metadata, _) in enumerate(keyword_results, start=1):
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0
                doc_details[doc_id] = (doc_text, metadata)
            rrf_scores[doc_id] += 1.0 / (rr_constant + rank)
            
        # Apply RRF rankings to vector results
        for rank, (doc_id, doc_text, metadata, _) in enumerate(vector_results, start=1):
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0
                doc_details[doc_id] = (doc_text, metadata)
            rrf_scores[doc_id] += 1.0 / (rr_constant + rank)
            
        # Sort by RRF scores
        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        final_results = []
        for doc_id, score in sorted_docs[:top_k]:
            text, meta = doc_details[doc_id]
            final_results.append({
                "id": doc_id,
                "text": text,
                "metadata": meta,
                "rrf_score": score
            })
            
        return final_results

# Interactive Test Block
if __name__ == "__main__":
    try:
        retriever = HybridRetriever()
        test_queries = [
            "What is the remote work stipend?",
            "What is the daily meal allowance limit?",
            "What password complexity is required?"
        ]
        
        for q in test_queries:
            print(f"\nQUERY: {q}")
            results = retriever.hybrid_search(q, top_k=2)
            for idx, r in enumerate(results):
                print(f"Rank {idx+1} [RRF Score: {r['rrf_score']:.4f}] ({r['metadata']['section']}):")
                print(f"Text: {r['text'][:150]}...")
    except Exception as e:
        print(f"Error executing search. Ensure data is ingested first. Details: {e}")
