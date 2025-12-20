from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

print("RPC:", BLOCKCHAIN_URL)
print("Contract:", CONTRACT_ADDRESS)

w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
code = w3.eth.get_code(CONTRACT_ADDRESS)

print("Bytecode length:", len(code))
print("Bytecode preview:", code[:10])
