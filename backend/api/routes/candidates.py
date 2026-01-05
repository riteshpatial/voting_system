from flask import Blueprint, jsonify
from backend.blockchain.web3_config import CONTRACT

candidates_bp = Blueprint("candidates", __name__)

@candidates_bp.route("/candidates", methods=["GET"])
def get_candidates():
    names, votes = CONTRACT.functions.getAllCandidates().call()

    result = []
    for i in range(len(names)):
        result.append({
            "id": i,
            "name": names[i],
            "votes": votes[i]
        })

    return jsonify(result)
