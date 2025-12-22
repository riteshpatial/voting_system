from web3 import Web3
from dotenv import load_dotenv
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
assert w3.is_connected(), "Blockchain not connected"

ADMIN_ACCOUNT = w3.eth.account.from_key(ADMIN_PRIVATE_KEY)
ADMIN_ADDRESS = ADMIN_ACCOUNT.address

ABI_PATH = os.path.join(BASE_DIR, "abi", "VotingABI.json")
with open(ABI_PATH) as f:
    ABI = json.load(f)

CONTRACT = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=ABI
)

def _send_tx(fn):
    tx = fn.build_transaction({
        "from": ADMIN_ADDRESS,
        "nonce": w3.eth.get_transaction_count(ADMIN_ADDRESS),
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "chainId": w3.eth.chain_id
    })
    signed = ADMIN_ACCOUNT.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()

def add_candidate(name):
    return {"tx": _send_tx(CONTRACT.functions.addCandidate(name))}

def start_election():
    return {"tx": _send_tx(CONTRACT.functions.startElection())}

def end_election():
    return {"tx": _send_tx(CONTRACT.functions.endElection())}

def reset_election():
    return {"tx": _send_tx(CONTRACT.functions.resetElection())}

def get_candidates():
    names, votes = CONTRACT.functions.getAllCandidates().call()
    return [{"id": i, "name": names[i], "votes": votes[i]} for i in range(len(names))]

def get_state():
    return int(CONTRACT.functions.getElectionState().call())
