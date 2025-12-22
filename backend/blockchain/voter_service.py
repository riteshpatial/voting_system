from web3 import Web3
from web3.exceptions import ContractLogicError
from dotenv import load_dotenv
import os, json

load_dotenv("backend/blockchain/.env")

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected(), "Blockchain not connected"

BASE_DIR = os.path.dirname(__file__)
ABI_PATH = os.path.join(BASE_DIR, "abi", "VotingABI.json")

with open(ABI_PATH) as f:
    ABI = json.load(f)

CONTRACT = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=ABI
)

def vote_candidate(candidate_id, private_key):
    try:
        voter = w3.eth.account.from_key(private_key)

        tx = CONTRACT.functions.vote(candidate_id).build_transaction({
            "from": voter.address,
            "nonce": w3.eth.get_transaction_count(voter.address),
            "gas": 300000,
            "gasPrice": w3.to_wei("20", "gwei"),
            "chainId": w3.eth.chain_id
        })

        signed = voter.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash)

        return {"message": "Vote cast successfully"}, 200

    except ContractLogicError as e:
        if "already voted" in str(e).lower():
            return {"message": "You have already voted"}, 409
        return {"message": "Vote rejected"}, 400

    except Exception:
        return {"message": "Blockchain connection error"}, 500
