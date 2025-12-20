from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected(), "Ganache not connected"

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=abi
)

admin = os.getenv("ADMIN_ADDRESS")
key = os.getenv("ADMIN_PRIVATE_KEY")

nonce = w3.eth.get_transaction_count(admin)

tx = contract.functions.endElection().build_transaction({
    "from": admin,
    "nonce": nonce,
    "gas": 200000,
    "gasPrice": w3.to_wei("20", "gwei"),
    "chainId": 1337
})

signed = w3.eth.account.sign_transaction(tx, key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Election ended")
print("TX:", receipt.transactionHash.hex())
