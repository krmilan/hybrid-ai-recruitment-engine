import os
import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

class HybridSearchEngine:
    def __init__(self, candidates):
        print("🧠 Initializing Universally Optimized AI Search Engine...")
        self.candidates = candidates
        
        # 1. Structure text components safely
        self.corpus = []
        for c in candidates:
            # Universal fallback string reading
            text_block = f"Skills: {c.get('skills', '')}. " \
                         f"Profile: {c.get('profile', '')}. " \
                         f"History: {c.get('career_history', '')}."
            self.corpus.append(text_block)
            
        # 2. Fast list-comprehension tokenization
        print("🔍 Compiling profiles for Keyword Search (BM25)...")
        tokenized_corpus = [doc.lower().split(" ") for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
        # 3. Model Vectorization
        print("🧬 Deploying Semantic AI Embedding Infrastructure...")
        self.vector_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # --- DISK CACHE OPTIMIZATION ---
        cache_file = "data/candidate_embeddings.npy"
        if os.path.exists(cache_file):
            print("💾 Embedding cache verified on disk. Loading instantly...")
            self.embeddings = np.load(cache_file)
        else:
            print("⏳ No cache localized. Vectorizing 100,000 records (Only happens once)...")
            self.embeddings = self.vector_model.encode(
                self.corpus, 
                show_progress_bar=True, 
                convert_to_numpy=True
            )
            np.save(cache_file, self.embeddings)
            print(f"💾 Matrices saved to cache file: {cache_file}")
            
        # --- FAISS RETRIEVAL INDEX OPTIMIZATION ---
        print("⚡ Constructing FAISS Index Matrix...")
        dimension = self.embeddings.shape[1]
        faiss.normalize_L2(self.embeddings)
        self.faiss_index = faiss.IndexFlatIP(dimension)
        self.faiss_index.add(self.embeddings)

    def search(self, job_description, top_k=100):
        # Keyword matching score array
        tokenized_query = job_description.lower().split(" ")
        bm25_scores = np.array(self.bm25.get_scores(tokenized_query))
        
        # Normalize BM25 values safely
        if bm25_scores.max() != bm25_scores.min():
            bm25_scores = (bm25_scores - bm25_scores.min()) / (bm25_scores.max() - bm25_scores.min())
        
        # FAISS search computation
        query_embedding = self.vector_model.encode([job_description], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        raw_semantic_scores, indices = self.faiss_index.search(query_embedding, len(self.candidates))
        
        semantic_scores = np.zeros(len(self.candidates))
        for score, idx in zip(raw_semantic_scores[0], indices[0]):
            semantic_scores[idx] = score
            
        # Dual-layer score blend
        final_scores = (0.5 * bm25_scores) + (0.5 * semantic_scores)
        top_indices = np.argsort(final_scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "candidate": self.candidates[idx],
                "score": float(final_scores[idx])
            })
        return results