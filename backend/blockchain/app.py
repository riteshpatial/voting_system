from flask import Flask, request, jsonify
from flask_cors import CORS

from admin_service import *
from voter_service import vote_candidate

app = Flask(__name__)
CORS(app)

@app.route("/api/add-candidate", methods=["POST"])
def add_candidate_api():
    return jsonify(add_candidate(request.json["name"]))

@app.route("/api/start-election", methods=["POST"])
def start_election_api():
    return jsonify(start_election())

@app.route("/api/end-election", methods=["POST"])
def end_election_api():
    return jsonify(end_election())

@app.route("/api/reset-election", methods=["POST"])
def reset_election_api():
    return jsonify(reset_election())

@app.route("/api/candidates")
def candidates_api():
    return jsonify(get_candidates())

@app.route("/api/state")
def state_api():
    return jsonify({"state": get_state()})

@app.route("/api/vote", methods=["POST"])
def vote_api():
    result, status = vote_candidate(
        request.json["candidate_id"],
        request.json["private_key"]
    )
    return jsonify(result), status

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
