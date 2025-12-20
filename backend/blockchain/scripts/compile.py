from solcx import compile_standard, install_solc
import json

install_solc("0.8.20")

with open("backend/blockchain/contracts/Voting.sol", encoding="utf-8") as f:
    source = f.read()

compiled = compile_standard({
    "language": "Solidity",
    "sources": {
        "Voting.sol": {"content": source}
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
}, solc_version="0.8.20")

abi = compiled["contracts"]["Voting.sol"]["Voting"]["abi"]
bytecode = compiled["contracts"]["Voting.sol"]["Voting"]["evm"]["bytecode"]["object"]

with open("backend/blockchain/abi/VotingABI.json", "w") as f:
    json.dump(abi, f)

with open("backend/blockchain/abi/VotingBytecode.txt", "w") as f:
    f.write(bytecode)

print("✅ ABI & BYTECODE GENERATED (MATCHED)")
