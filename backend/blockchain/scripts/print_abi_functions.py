from web3 import Web3
from dotenv import load_dotenv
import json, os

load_dotenv("backend/blockchain/.env")

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))

with open("backend/blockchain/abi/VotingABI.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS")),
    abi=abi
)

print("\n🔍 FUNCTIONS IN ABI:\n")
for fn in contract.functions:
    print(fn)
