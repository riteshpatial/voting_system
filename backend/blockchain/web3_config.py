from web3 import Web3
import json
import os

# ======================
# CONFIG
# ======================
GANACHE_URL = "http://127.0.0.1:8545"
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

ADMIN_PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")
ADMIN_ADDRESS = os.getenv("ADMIN_ADDRESS")

# ======================
# WEB3 CONNECTION
# ======================
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

if not w3.is_connected():
    raise RuntimeError("❌ Web3 not connected to Ganache")

# ======================
# LOAD ABI (LIST FORMAT)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ABI_PATH = os.path.join(BASE_DIR, "abi", "VotingABI.json")

if not os.path.exists(ABI_PATH):
    raise FileNotFoundError(f"❌ ABI file not found at {ABI_PATH}")

with open(ABI_PATH, "r") as f:
    abi = json.load(f)   # ✅ DIRECT LOAD, NO ["abi"]

# ======================
# CONTRACT INSTANCE
# ======================
CONTRACT = w3.eth.contract(
    address=w3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)