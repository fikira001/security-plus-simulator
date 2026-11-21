"""
OpenSecPlus — Database Verification Utility
Verifies that questions, performance-based questions, study guides,
and acronym resources parse cleanly without errors.
"""

import os
import json
import sys

def verify():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "exam_simulator", "data")
    
    files = {
        "questions_db.json": ["all_mcqs", "pbqs", "acronyms"],
        "domain_study_guides.json": None,
        "acronyms.json": None
    }
    
    all_ok = True
    print("=" * 60)
    print("OpenSecPlus — Data Integrity Verification")
    print("=" * 60)
    
    for filename, required_keys in files.items():
        path = os.path.join(data_dir, filename)
        if not os.path.exists(path):
            print(f"[FAIL] Missing {filename}")
            all_ok = False
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if required_keys:
                for k in required_keys:
                    if k not in data:
                        print(f"[FAIL] {filename} missing required key: {k}")
                        all_ok = False
            if filename == "questions_db.json":
                mcqs = len(data.get("all_mcqs", []))
                pbqs = len(data.get("pbqs", []))
                acros = len(data.get("acronyms", []))
                print(f"[OK] {filename} (MCQs: {mcqs}, PBQs: {pbqs}, Acronyms: {acros})")
            elif filename == "domain_study_guides.json":
                domains = list(data.keys())
                print(f"[OK] {filename} (Domains loaded: {domains})")
            elif filename == "acronyms.json":
                print(f"[OK] {filename} ({len(data)} items)")
        except Exception as e:
            print(f"[FAIL] {filename} error: {e}")
            all_ok = False

    print("=" * 60)
    if all_ok:
        print("All data files verified successfully!")
    else:
        print("Data integrity check failed!")
        sys.exit(1)

if __name__ == "__main__":
    verify()
