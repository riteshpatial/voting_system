from web3 import Web3
from dotenv import load_dotenv
import json, os

print("\n📊 FINAL RESULTS")

# Load env
load_dotenv("backend/blockchain/.env")

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

print("USING CONTRACT:", CONTRACT_ADDRESS)

# Web3
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
assert w3.is_connected(), "❌ Ganache not connected"

# ABI
with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# ✅ CORRECT CALL
state = contract.functions.electionState().call()
assert state == 2, f"❌ Election not ended. Current state = {state}"

total = contract.functions.getCandidatesCount().call()
print("Total candidates:", total)

names, votes = contract.functions.getAllCandidates().call()

for i in range(len(names)):
    print(f"{i+1}. {names[i]} → Votes: {votes[i]}")

