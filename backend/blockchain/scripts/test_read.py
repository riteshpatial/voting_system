from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv()
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

print("🚨 test_read CONTRACT_ADDRESS =", CONTRACT_ADDRESS)

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
assert w3.is_connected()

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=os.getenv("CONTRACT_ADDRESS"),
    abi=abi
)
print("🚨 USING CONTRACT:", CONTRACT_ADDRESS)

print("USING CONTRACT:", CONTRACT_ADDRESS)
print("READING CONTRACT:", CONTRACT_ADDRESS)
print("Admin:", contract.functions.admin().call())
print("Election state:", contract.functions.electionState().call())
print("Candidates:", contract.functions.getCandidatesCount().call())
