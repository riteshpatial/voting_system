import json
import os

RESULTS_FILE = "backend/storage/results.json"

def get_election_state():
    # TEMP: API step 1 does NOT touch blockchain
    # We assume election is ended when results exist
    if os.path.exists(RESULTS_FILE):
        return 2  # ended
    return 0  # not started / unknown

def get_results():
    if not os.path.exists(RESULTS_FILE):
        return {
            "status": "no_results",
            "results": []
        }

    with open(RESULTS_FILE, "r") as f:
        data = json.load(f)

    results = [
        {"name": name, "votes": votes}
        for name, votes in data.items()
    ]

    return {
        "status": "success",
        "results": results
    }
