from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv("backend/blockchain/.env")

w3 = Web3(Web3.HTTPProvider(os.getenv("BLOCKCHAIN_URL")))
addr = Web3.to_checksum_address(os.getenv("ADMIN_ADDRESS"))

bal = w3.eth.get_balance(addr)
print("Admin:", addr)
print("Balance (ETH):", w3.from_wei(bal, 'ether'))
