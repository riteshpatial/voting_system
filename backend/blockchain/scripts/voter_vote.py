import sys
from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv("backend/blockchain/.env")

candidate_id = int(sys.argv[1])  # 👈 from API

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected()

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=abi
)

VOTER_PRIVATE_KEY = os.getenv("VOTER_PRIVATE_KEY")
VOTER_ADDRESS = w3.eth.account.from_key(VOTER_PRIVATE_KEY).address

nonce = w3.eth.get_transaction_count(VOTER_ADDRESS)

tx = contract.functions.vote(candidate_id).build_transaction({
    "from": VOTER_ADDRESS,
    "nonce": nonce,
    "gas": 300000,
    "gasPrice": w3.to_wei("20", "gwei")
})

signed_tx = w3.eth.account.sign_transaction(tx, VOTER_PRIVATE_KEY)
w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Vote successful")
