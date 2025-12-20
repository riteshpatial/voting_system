from web3 import Web3
from dotenv import load_dotenv
import json
import os
import csv
from datetime import datetime
print("🚨 CWD:", os.getcwd())
print("🚨 FILE:", __file__)
# ---------------- ENV ----------------
load_dotenv("backend/blockchain/.env")

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected(), "❌ Ganache not connected"

# ---------------- ABI ----------------
with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=abi
)

# ---------------- VOTER ----------------
VOTER_PRIVATE_KEY = os.getenv("VOTER_PRIVATE_KEY")
if not VOTER_PRIVATE_KEY:
    raise ValueError("❌ VOTER_PRIVATE_KEY missing in .env")

VOTER_ADDRESS = w3.eth.account.from_key(VOTER_PRIVATE_KEY).address
print("🗳️ Voting from:", VOTER_ADDRESS)

# ---------------- VOTE ----------------
nonce = w3.eth.get_transaction_count(VOTER_ADDRESS)

tx = contract.functions.vote(1).build_transaction({
    "from": VOTER_ADDRESS,
    "nonce": nonce,
    "gas": 300000,
    "gasPrice": w3.to_wei("20", "gwei")
})

signed_tx = w3.eth.account.sign_transaction(tx, VOTER_PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("✅ Vote cast")
print("TX:", tx_hash.hex())

# ---------------- OFF-CHAIN RESULT ----------------
RESULTS_FILE = "backend/storage/results.json"
VOTED_CANDIDATE = "Alice"

with open(RESULTS_FILE, "r") as f:
    data = json.load(f)

data[VOTED_CANDIDATE] += 1

with open(RESULTS_FILE, "w") as f:
    json.dump(data, f, indent=2)

print("✅ Vote recorded in backend results")

# ---------------- LOGGING (FIXED PATH) ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(BASE_DIR, "logs", "voting_logs.csv")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

row = [
    datetime.now().isoformat(),
    VOTER_ADDRESS,
    VOTED_CANDIDATE
]

file_exists = os.path.isfile(LOG_FILE)

with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["timestamp", "voter", "candidate"])
    writer.writerow(row)

print("📝 Vote logged at:", LOG_FILE)
