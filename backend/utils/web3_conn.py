from web3 import Web3
from dotenv import load_dotenv
import json
import os

# Load env
load_dotenv("backend/blockchain/.env")

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

# Web3 connection
w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
if not w3.is_connected():
    raise Exception("❌ Ganache not connected")

# Load ABI
ABI_PATH = "backend/blockchain/abi/VotingABI.json"
with open(ABI_PATH) as f:
    abi = json.load(f)

# Contract instance
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def get_contract():
    return contract

def get_web3():
    return w3
