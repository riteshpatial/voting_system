import os
from dotenv import load_dotenv

load_dotenv("backend/blockchain/.env")

print("ADMIN:", os.getenv("ADMIN_PRIVATE_KEY"))
print("VOTER:", os.getenv("VOTER_PRIVATE_KEY"))
