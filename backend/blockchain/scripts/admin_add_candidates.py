from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected(), "Ganache not connected"

ADMIN = Web3.to_checksum_address(os.getenv("ADMIN_ADDRESS"))
PK = os.getenv("ADMIN_PRIVATE_KEY")
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

print("ADMIN:", ADMIN)
print("CONTRACT ADMIN:", contract.functions.admin().call())
print("Election State:", contract.functions.electionState().call())

assert contract.functions.electionState().call() == 0, "Election already started"

names = ["Alice", "Bob"]

for name in names:
    nonce = w3.eth.get_transaction_count(ADMIN)

    tx = contract.functions.addCandidate(name).build_transaction({
        "from": ADMIN,
        "nonce": nonce,
        "gas": 500_000,
        "gasPrice": w3.eth.gas_price,
        "chainId": 1337
    })

    signed = w3.eth.account.sign_transaction(tx, PK)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"{name} → TX status:", receipt.status)

    if receipt.status != 1:
        raise Exception("❌ addCandidate reverted")

print("✅ ALL CANDIDATES ADDED SUCCESSFULLY")
