import jsonlines
from docx import Document
import os

def read_docx(file_path):
    """Helper function to read text from a Word document (.docx)"""
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File not found at {file_path}")
        return ""
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def load_challenge_data():
    print("📦 Reading challenge datasets...")
    
    # 1. Load the Job Description
    jd_text = read_docx("data/job_description.docx")
    print(f"✅ Loaded Job Description ({len(jd_text)} characters)")
    
    # 2. Load the Redrob Signals text (extra contextual info)
    signals_text = read_docx("data/redrob_signals_doc.docx")
    print(f"✅ Loaded Redrob Signals ({len(signals_text)} characters)")

    # 3. Load Candidates Profiles from candidates.jsonl
    candidates = []
    candidates_path = "data/candidates.jsonl"
    
    if os.path.exists(candidates_path):
        with jsonlines.open(candidates_path) as reader:
            for obj in reader:
                candidates.append(obj)
        print(f"✅ Loaded {len(candidates)} candidate profiles from JSONL")
    else:
        print(f"❌ Error: {candidates_path} not found!")

    return jd_text, signals_text, candidates

if __name__ == "__main__":
    # Test running the script directly
    jd, signals, candidates = load_challenge_data()
    if candidates:
        print("\n👀 Let's look at the structure of the first candidate profile:")
        print(list(candidates[0].keys()))