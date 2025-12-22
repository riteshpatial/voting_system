from web3 import Web3
from dotenv import load_dotenv
import json
import os

# Load .env
load_dotenv()

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")
ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")

assert BLOCKCHAIN_URL, "BLOCKCHAIN_URL missing"
assert ADMIN_ADDRESS, "ADMIN_ADDRESS missing"
assert ADMIN_PRIVATE_KEY, "ADMIN_PRIVATE_KEY missing"

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
assert w3.is_connected(), "❌ Ganache not connected"

print("✅ Connected to Ganache")

# Load ABI
abi_path = "backend/blockchain/abi/VotingABI.json"
with open(abi_path, "r") as f:
    contract_abi = json.load(f)

# ✅ LOAD BYTECODE FROM FILE (THIS WAS THE BUG)
bytecode_path = "backend/blockchain/abi/VotingBytecode.txt"
with open(bytecode_path, "r") as f:
    BYTECODE = f.read().strip()

assert BYTECODE.startswith("6080"), "❌ Invalid bytecode"

Voting = w3.eth.contract(abi=contract_abi, bytecode=BYTECODE)

nonce = w3.eth.get_transaction_count(ADMIN_ADDRESS)

tx = Voting.constructor().build_transaction({
    "from": ADMIN_ADDRESS,
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": 1337
})

signed_tx = w3.eth.account.sign_transaction(tx, ADMIN_PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ CONTRACT DEPLOYED")
print("📌 Contract Address:", receipt.contractAddress)
