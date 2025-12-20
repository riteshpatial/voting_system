from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv("backend/blockchain/.env")

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected()

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=abi
)

state = contract.functions.electionState().call()
count = contract.functions.getCandidatesCount().call()

print("Election state:", state)
print("Candidates count:", count)

if state == 2 and count > 0:
    names, votes = contract.functions.getAllCandidates().call()
    print("RESULTS:")
    for i in range(len(names)):
        print(f"{names[i]} → {votes[i]}")
else:
    print("⚠️ Results not available yet")
