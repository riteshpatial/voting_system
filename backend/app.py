from flask import Flask, request, jsonify
from backend.utils.web3_helper import get_contract, get_web3
from backend.config import ADMIN_ADDRESS, ADMIN_PRIVATE_KEY
import csv
from datetime import datetime

app = Flask(__name__)

contract = get_contract()
w3 = get_web3()

LOG_FILE = "backend/logs/voting_logs.csv"


def log_activity(voter, action):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([voter, action, datetime.now()])


@app.route("/register_voter", methods=["POST"])
def register_voter():
    data = request.json
    voter_address = data["voter_address"]

    nonce = w3.eth.get_transaction_count(ADMIN_ADDRESS)

    txn = contract.functions.registerVoter(
        voter_address
    ).build_transaction({
        "from": ADMIN_ADDRESS,
        "nonce": nonce,
        "gas": 3000000
    })

    signed_txn = w3.eth.account.sign_transaction(txn, ADMIN_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    log_activity(voter_address, "REGISTER")

    return jsonify({
        "status": "Voter registered",
        "tx_hash": tx_hash.hex()
    })


@app.route("/vote", methods=["POST"])
def vote():
    data = request.json
    voter_address = data["voter_address"]
    private_key = data["private_key"]
    candidate_id = int(data["candidate_id"])

    nonce = w3.eth.get_transaction_count(voter_address)

    txn = contract.functions.vote(candidate_id).build_transaction({
        "from": voter_address,
        "nonce": nonce,
        "gas": 3000000
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    log_activity(voter_address, f"VOTE_{candidate_id}")

    return jsonify({
        "status": "Vote casted",
        "tx_hash": tx_hash.hex()
    })


@app.route("/results", methods=["GET"])
def results():
    candidates = []
    count = contract.functions.getCandidatesCount().call()

    for i in range(1, count + 1):
        c = contract.functions.getCandidate(i).call()
        candidates.append({
            "id": c[0],
            "name": c[1],
            "votes": c[2]
        })

    return jsonify(candidates)


if __name__ == "__main__":
    app.run(debug=True)
