from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=os.getenv("CONTRACT_ADDRESS"),
    abi=abi
)

ADMIN = os.getenv("ADMIN_ADDRESS")
PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")

nonce = w3.eth.get_transaction_count(ADMIN)

def send_tx(fn):
    global nonce
    tx = fn.build_transaction({
        "from": ADMIN,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei"),
        "chainId": 1337
    })
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    nonce += 1
    print("TX OK:", tx_hash.hex())

# ---- ADMIN FLOW ----
send_tx(contract.functions.addCandidate("Alice"))
send_tx(contract.functions.addCandidate("Bob"))
send_tx(contract.functions.startElection())
