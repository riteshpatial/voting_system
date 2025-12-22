from web3 import Web3
from web3.exceptions import ContractLogicError
from dotenv import load_dotenv
import json, os

load_dotenv("backend/blockchain/.env")

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))

if not w3.is_connected():
    raise Exception("Blockchain not connected")

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)


def vote_candidate(candidate_id: int, private_key: str):
    try:
        voter_account = w3.eth.account.from_key(private_key)
        voter_address = voter_account.address

        nonce = w3.eth.get_transaction_count(voter_address)

        tx = contract.functions.vote(candidate_id).build_transaction({
            "from": voter_address,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": w3.to_wei("20", "gwei")
        })

        signed_tx = voter_account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

        w3.eth.wait_for_transaction_receipt(tx_hash)

        return {
            "status": "success",
            "tx_hash": tx_hash.hex()
        }, 200

    except ContractLogicError as e:
        msg = str(e).lower()

        if "already voted" in msg:
            return {
                "error": "You have already voted"
            }, 409

        return {
            "error": "Smart contract rejected the vote",
            "details": str(e)
        }, 400

    except Exception as e:
        return {
            "error": "Blockchain connection error",
            "details": str(e)
        }, 500
