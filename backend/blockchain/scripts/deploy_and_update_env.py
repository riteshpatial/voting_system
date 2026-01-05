import json
import os
from web3 import Web3
from dotenv import load_dotenv, set_key

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected(), "Blockchain not connected"

with open(os.path.join(BASE_DIR, "build/contracts/Voting.json")) as f:
    artifact = json.load(f)

abi = artifact["abi"]
bytecode = artifact["bytecode"]

admin_pk = os.getenv("ADMIN_PRIVATE_KEY")
admin = w3.eth.account.from_key(admin_pk)

Voting = w3.eth.contract(abi=abi, bytecode=bytecode)

tx = Voting.constructor().build_transaction({
    "from": admin.address,
    "nonce": w3.eth.get_transaction_count(admin.address),
    "gas": 4000000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": w3.eth.chain_id
})

signed = admin.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

new_address = receipt.contractAddress

set_key(ENV_PATH, "CONTRACT_ADDRESS", new_address)

print("✅ New Election Contract Deployed")
print("🆕 CONTRACT_ADDRESS =", new_address)
