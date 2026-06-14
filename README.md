# 🚀 Multi-Stage Hybrid AI Recruitment Engine

> An enterprise-scale AI-powered recruitment engine that intelligently ranks **100,000+ candidate profiles** against job descriptions using hybrid retrieval, semantic search, and deep neural re-ranking.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow)
![Scale](https://img.shields.io/badge/Scale-100K%2B_Candidates-red)

---

## About

This project was developed as a solution to a recruitment AI engineering challenge. The objective was to design a scalable system capable of ranking and matching candidates against job descriptions while maintaining high retrieval quality across large datasets.

---

## 📖 Overview

Traditional Applicant Tracking Systems (ATS) rely heavily on exact keyword matching, often missing highly qualified candidates simply because they use different terminology.

This project introduces a **multi-stage AI recruitment pipeline** that combines:

- 🔍 BM25 Keyword Search
- 🧠 Semantic Vector Search
- ⚡ FAISS Similarity Retrieval
- 🎯 Cross-Encoder Re-Ranking

The system evaluates candidates more like an experienced recruiter rather than a traditional ATS.

---

## 🎯 Key Features

- ✅ Scales to **100,000+ candidate profiles**
- ✅ Hybrid retrieval using BM25 + Semantic Search
- ✅ FAISS-powered millisecond vector search
- ✅ Deep contextual ranking with Cross-Encoders
- ✅ Embedding caching for faster execution
- ✅ Universal candidate data ingestion
- ✅ Explainable ranking outputs
- ✅ Production-oriented architecture

---

## 🏗️ Architecture

```text
                 ┌─────────────────┐
                 │ Job Description │
                 └────────┬────────┘
                          │
                          ▼
┌───────────────┐   ┌───────────────┐
│ Candidate DB  │──▶│ Data Loader   │
└───────────────┘   └───────┬───────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Hybrid Retrieval    │
                 │ BM25 + FAISS Search │
                 └─────────┬───────────┘
                           │
                           ▼
                    Top 100 Candidates
                           │
                           ▼
                 ┌─────────────────────┐
                 │ Cross-Encoder       │
                 │ Re-Ranking Layer    │
                 └─────────┬───────────┘
                           │
                           ▼
                 ┌─────────────────────┐
                 │ Ranked Output CSV   │
                 └─────────────────────┘
```

---

## 🚨 The Problem

Most ATS systems suffer from two major issues:

### 1. Vocabulary Mismatch

A candidate may write:

> Distributed Event Streaming Systems

while a job description requires:

> Kafka

Traditional keyword filters may reject the candidate despite the relevant experience.

### 2. Scalability Limitations

Deep neural ranking models are computationally expensive when applied directly across large candidate pools.

Running contextual matching on **100,000 candidates** becomes impractical without an optimized retrieval pipeline.

---

## 💡 Solution

The system uses a **two-stage ranking architecture**.

### Stage 1 — Hybrid Retrieval

#### BM25 Search

Captures:

- Technical keywords
- Libraries
- Frameworks
- Certifications
- Acronyms

#### Semantic Search

Uses:

```python
all-MiniLM-L6-v2
```

to generate dense embeddings capable of understanding:

- Synonyms
- Context
- Intent
- Related technologies

Examples:

| Job Requirement | Candidate Experience |
|---------------|--------------------|
| Kubernetes | Container Orchestration |
| Kafka | Event Streaming Systems |
| AWS | Cloud Infrastructure |

Both scores are normalized and combined:

```text
Final Retrieval Score =
0.5 × BM25 +
0.5 × Semantic Similarity
```

The engine then selects the **Top 100 candidates**.

---

### Stage 2 — Deep Re-Ranking

The shortlisted candidates are passed through:

```python
ms-marco-MiniLM-L-6-v2
```

Unlike traditional embeddings, a Cross-Encoder processes:

```text
(Job Description, Candidate Profile)
```

together, enabling deep evaluation of:

- Skill alignment
- Experience relevance
- Career trajectory
- Contextual fit

This significantly improves ranking quality.

---

## ⚡ Performance Optimizations

### Embedding Cache

Generated embeddings are stored locally:

```text
candidate_embeddings.npy
```

Benefits:

- Compute embeddings once
- Reload instantly on future runs
- Drastically reduce execution time

---

### FAISS Vector Search

Instead of brute-force cosine similarity calculations, the system uses:

```python
faiss.IndexFlatIP
```

Advantages:

- Millisecond retrieval
- Optimized vector operations
- Efficient scaling for large datasets

---

## 🛡️ Honeypot & Fraud Defense Layer

The system implements an automated defensive gate within the data ingestion layer (`src/data_loader.py`) to handle malicious "honeypot" candidates planted in the dataset.

* **The Problem:** Keyword-stuffer profiles use extreme technical phrase densities to artificially trick semantic embeddings into ranking them at the very top, despite having faked information.
* **The Solution:** Before any matrix vectorization occurs, the pipeline intercepts the data stream and evaluates the nested `redrob_signals` attributes. Any profile carrying affirmative flags for `impossible_timeline` or `fake_experience` is permanently purged from the tracking pool. 
* **The Impact:** This completely protects downstream ranking matrices from corruption and guarantees compliance with the strict $<10\%$ challenge disqualification threshold.

---

## 📂 Project Structure

```text
project/
│
├── data/
│   ├── job_description.docx
│   ├── candidates.jsonl
│   └── final_submission.csv
│
├── src/
│   ├── data_loader.py
│   ├── hybrid_search.py
│   ├── reranker.py
│
├── candidate_embeddings.npy
├── main.py
├── requirements.txt
└── README.md
```

---

## 📥 Input Requirements

### Job Description

File:

```text
job_description.docx
```

Contains:

- Required skills
- Responsibilities
- Qualifications
- Experience requirements

---

### Candidate Dataset

File:

```text
candidates.jsonl
```

Expected format:

```json
{
  "candidate_id": "12345",
  "skills": "...",
  "profile": "...",
  "career_history": "..."
}
```

---

## 📤 Output

Generated file:

```text
data/final_submission.csv
```

### Output Schema

| Column | Description |
|----------|-------------|
| candidate_id | Unique candidate identifier |
| rank | Candidate ranking position |
| score | Normalized score (0.0000 - 1.0000) |
| reasoning | Explainable ranking summary |

Example:

```csv
candidate_id,rank,score,reasoning
A102,1,0.9812,Strong semantic alignment with cloud infrastructure experience.
```

---

## 🛠 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/ai-recruitment-engine.git

cd ai-recruitment-engine
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Additional dependencies:

```bash
pip install faiss-cpu python-docx jsonlines
```

---

## ▶️ Running the Pipeline

Place:

```text
data/job_description.docx

data/candidates.jsonl
```

inside the `data/` directory.

Run:

```bash
python main.py
```

### First Run

- Generates embeddings
- Builds FAISS index
- Creates cache

### Subsequent Runs

- Loads cached embeddings
- Skips vector generation
- Executes significantly faster

---

## 📈 Scalability

| Candidate Count | Supported |
|---------------|------------|
| 1,000 | ✅ |
| 10,000 | ✅ |
| 50,000 | ✅ |
| 100,000+ | ✅ |

The architecture is specifically designed to handle large-scale recruitment workloads efficiently.

---

## 🔮 Future Enhancements

- Multi-JD processing
- GPU-accelerated FAISS indexing
- Recruiter dashboard
- REST API deployment
- Candidate skill-gap analysis
- LLM-generated recruiter insights
- Interview recommendation engine

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to fork the repository and submit pull requests.

---

## 📜 License

Distributed under the MIT License.

See `LICENSE` for more information.

---

## ⭐ Support

If you find this project useful, consider giving it a **star** ⭐ on GitHub.
It helps others discover the project and supports future development.