from sentence_transformers import CrossEncoder

class DeepReRanker:
    def __init__(self):
        print("🧬 Loading Deep Contextual Cross-Encoder Re-ranker...")
        # Using a highly-optimized, fast re-ranking model
        self.model = CrossEncoder("ms-marco-MiniLM-L-6-v2")

    def rerank(self, job_description, top_matches):
        print("🧠 Re-ranking top candidates using deep contextual alignment...")
        
        # Prepare the pairs for the Cross-Encoder model: [ [JD, Candidate1], [JD, Candidate2], ... ]
        pairs = []
        for match in top_matches:
            c = match["candidate"]
            candidate_text = f"Skills: {c.get('skills', '')}. Profile: {c.get('profile', '')}. History: {c.get('career_history', '')}"
            pairs.append([job_description, candidate_text])
            
        # Predict deep similarity scores (higher score means better alignment)
        scores = self.model.predict(pairs)
        
        # Update the scores in our matches list
        for idx, score in enumerate(scores):
            top_matches[idx]["rerank_score"] = float(score)
            
        # Sort the candidates again based on the smarter re-ranker score
        top_matches.sort(key=lambda x: x["rerank_score"], reverse=True)
        return top_matches

if __name__ == "__main__":
    print("Re-ranker script is operational and ready.")