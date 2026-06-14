import os
import jsonlines
from docx import Document

def read_docx(file_path):
    if not os.path.exists(file_path):
        print(f"⚠️ Warning: File not found at {file_path}")
        return ""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def load_challenge_data():
    print("📦 Reading challenge workspace files from disk...")
    
    jd_path = "data/job_description.docx"
    signals_path = "data/redrob_signals_doc.docx"
    candidates_path = "data/candidates.jsonl"
    
    # 1. Parse documentation texts
    jd_text = read_docx(jd_path)
    signals_text = read_docx(signals_path)
    
    # 2. Ingest candidate dataset with defensive honeypot filtering
    candidates = []
    skipped_honeypots = 0
    
    if os.path.exists(candidates_path):
        print("🕵️‍♂️ Scanning 100,000 records for malicious honeypot profiles...")
        with jsonlines.open(candidates_path) as reader:
            for obj in reader:
                # Extract the behavioral signals block
                signals = obj.get("redrob_signals", {})
                
                # If signals dictate an impossible profile or faked history, drop them immediately!
                if isinstance(signals, dict):
                    if signals.get("impossible_timeline", 0) == 1 or signals.get("fake_experience", 0) == 1:
                        skipped_honeypots += 1
                        continue # Skip this profile entirely; do not add to candidates
                
                candidates.append(obj)
                
        print(f"  ✅ Extraction Complete: Retained {len(candidates)} valid candidate profiles.")
        print(f"  🛑 Guardrails Engaged: Intercepted and scrubbed {skipped_honeypots} honeypot traps.")
    else:
        print(f"❌ Critical Error: Data source missing at {candidates_path}")
        
    return jd_text, signals_text, candidates