import json
import fsspec

with fsspec.open('hf://datasets/AQ-MedAI/RAG-QA-Leaderboard/final_data/documents_pool.json', 'r') as f:
    d = json.load(f)
    print("Num documents:", len(d))
    first_key = list(d.keys())[0]
    print(f"First document ({first_key}):", d[first_key][:150] + "...")
