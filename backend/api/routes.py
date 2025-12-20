from flask import Blueprint, jsonify, request
from backend.blockchain.tx_service import get_results, get_election_state

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "API is running"
    })

@api.route("/status", methods=["GET"])
def status():
    state = get_election_state()
    return jsonify({
        "election_state": state
    })

@api.route("/results", methods=["GET"])
def results():
    data = get_results()
    return jsonify(data)
