from flask import Blueprint, jsonify, request
from backend.blockchain.vote_service import cast_vote
from backend.blockchain.tx_service import get_results
from backend.blockchain.voter_service import register_voter
from backend.blockchain.admin_service import (
    add_candidate,
    start_election,
    end_election,
    get_candidates
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.route("/candidates")
def candidates():
    return jsonify(get_candidates())


@api_bp.route("/vote", methods=["POST"])
def vote():
    data = request.json
    return jsonify(cast_vote(int(data["candidate_id"])))


@api_bp.route("/results")
def results():
    return jsonify(get_results())


# ---------- ADMIN ----------
@api_bp.route("/admin/add-candidate", methods=["POST"])
def admin_add_candidate():
    return jsonify(add_candidate(request.json["name"]))


@api_bp.route("/admin/start-election", methods=["POST"])
def admin_start():
    return jsonify(start_election())


@api_bp.route("/admin/end-election", methods=["POST"])
def admin_end():
    return jsonify(end_election())


@api_bp.route("/admin/register-voter", methods=["POST"])
def admin_register_voter():
    voter_address = request.json.get("voter_address")
    tx = register_voter(voter_address)

    return jsonify({
        "status": "success",
        "tx_hash": tx
    })
@api_bp.route("/register-voter", methods=["POST"])
def register_voter_api():
    data = request.get_json()

    if not data or "voter_address" not in data:
        return jsonify({
            "status": "error",
            "message": "voter_address required"
        }), 400

    try:
        tx_hash = register_voter(data["voter_address"])
        return jsonify({
            "status": "success",
            "tx_hash": tx_hash
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500