from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
ADMIN = os.getenv("ADMIN_ADDRESS")
PRIVATE_KEY = os.getenv("ADMIN_PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

assert BLOCKCHAIN_URL, "BLOCKCHAIN_URL missing"
assert ADMIN, "ADMIN_ADDRESS missing"
assert PRIVATE_KEY, "ADMIN_PRIVATE_KEY missing"
assert CONTRACT_ADDRESS, "CONTRACT_ADDRESS missing"

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
assert w3.is_connected(), "Ganache not connected"

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

nonce = w3.eth.get_transaction_count(ADMIN)

tx = contract.functions.resetElection().build_transaction({
    "from": ADMIN,
    "nonce": nonce,
    "gas": 300000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": 1337
})

signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Election RESET")
print("TX:", tx_hash.hex())
