# Blockchain Voting System

Ek decentralized voting system jo Ethereum blockchain par based hai. Is system mein smart contract ke through votes cast hote hain, Flask REST API se backend manage hota hai, aur anomaly detection bhi built-in hai.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Smart Contract Deploy Karna](#smart-contract-deploy-karna)
- [Server Chalana](#server-chalana)
- [API Endpoints](#api-endpoints)
- [Anomaly Detection](#anomaly-detection)
- [Sample Data](#sample-data)

---

## Project Overview

Yeh system ek transparent aur tamper-proof voting platform hai jisme:

- **Smart Contract** (Solidity) blockchain par election manage karta hai
- **Flask API** backend se client requests handle karta hai
- **Web3.py** Python aur blockchain ke beech connection banata hai
- **Anomaly Detection** script suspicious voting patterns detect karti hai (multiple votes, rapid voting)

---

## Project Structure

```
voting_system/
│
├── backend/
│   ├── api/
│   │   ├── app.py                  # Flask app factory
│   │   └── routes/
│   │       ├── routes.py           # Main API routes (vote, candidates, results, admin)
│   │       └── candidates.py       # Candidates read route
│   │
│   ├── blockchain/
│   │   ├── contracts/
│   │   │   └── Voting.sol          # Solidity smart contract
│   │   ├── abi/
│   │   │   ├── VotingABI.json      # Contract ABI
│   │   │   └── VotingBytecode.txt  # Contract bytecode
│   │   ├── scripts/
│   │   │   ├── deploy.py           # Contract deploy script
│   │   │   ├── admin_add_candidates.py
│   │   │   ├── admin_start_election.py
│   │   │   ├── admin_end_election.py
│   │   │   └── ...                 # Other admin/debug scripts
│   │   ├── admin_service.py        # Admin blockchain functions
│   │   ├── vote_service.py         # Voter casting functions
│   │   ├── voter_service.py        # Voter registration
│   │   ├── tx_service.py           # Results from JSON storage
│   │   ├── web3_config.py          # Web3 connection setup
│   │   └── .env                    # Blockchain config (private)
│   │
│   ├── logs/
│   │   └── voting_logs.csv         # Har vote ka log record
│   ├── storage/
│   │   └── results.json            # Election results JSON
│   ├── anomaly.py                  # Anomaly detection script
│   ├── config.py                   # dotenv config loader
│   └── requirements.txt
│
├── frontend/
│   └── dashboard/                  # Django-based dashboard (scaffold)
│
├── dashboard/
│   └── migrations/
│
├── docs/
│   ├── architecture.md
│   ├── workflow.md
│   ├── ml_explanation.md
│   ├── report.md
│   └── results.md
│
├── tests/                          # Test files
├── ml/                             # ML related code
├── run.py                          # Entry point
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Smart Contract | Solidity ^0.8.19 |
| Blockchain (local) | Ganache (chainId: 1337) |
| Contract Interaction | Web3.py |
| Backend API | Flask (Python) |
| Config Management | python-dotenv |
| Anomaly Detection | pandas |
| Contract Framework | Truffle |

---

## Prerequisites

Ye sab install hona chahiye aapke system par:

- **Python 3.10** (recommended — project 3.10 pe banaya gaya hai)
- **Node.js** (Ganache ke liye)
- **Ganache** (local blockchain)
- **pip** (Python package manager)

### Ganache Install Karna

```bash
npm install -g ganache
```

Ya Ganache GUI download karo: https://trufflesuite.com/ganache/

---

## Setup & Installation

### Step 1 — Repo Clone Karo (pehle se ho chuka hai)

```bash
git clone https://github.com/riteshpatial/voting_system
cd voting_system
```

### Step 2 — Python Dependencies Install Karo

```bash
pip install flask web3 python-dotenv pandas
```

### Step 3 — Ganache Chalao

Terminal mein:
```bash
ganache --port 8545 --chainId 1337
```

Ganache start hone par aapko accounts aur private keys milenge. Inhe copy karke `.env` mein daalna hoga.

---

## Environment Variables

File path: `backend/blockchain/.env`

```env
BLOCKCHAIN_URL=http://127.0.0.1:8545
ADMIN_ADDRESS=0xYourAdminAddress
ADMIN_PRIVATE_KEY=0xYourAdminPrivateKey
CONTRACT_ADDRESS=0xDeployedContractAddress
VOTER_PRIVATE_KEY=0xYourVoterPrivateKey
VOTER_ADDRESS=0xYourVoterAddress
```

> **Note:** Ganache restart hone par addresses badal jaate hain — fresh deploy ke baad CONTRACT_ADDRESS update karo.

---

## Smart Contract Deploy Karna

Ganache chal raha ho tab yeh script chalao:

```bash
python backend/blockchain/scripts/deploy.py
```

Output mein `Contract Address` milega — use `.env` ke `CONTRACT_ADDRESS` mein update karo.

### Candidates Add Karna (Election se pehle)

```bash
python backend/blockchain/scripts/admin_add_candidates.py
```

Default candidates: **Alice** aur **Bob**

### Election Start Karna

```bash
python backend/blockchain/scripts/admin_start_election.py
```

### Election End Karna

```bash
python backend/blockchain/scripts/admin_end_election.py
```

---

## Server Chalana

```bash
cd voting_system
python -m backend.api.app
```

Server `http://127.0.0.1:5000` par chalega.

---

## API Endpoints

### Health Check

```
GET /api/health
```
```json
{ "status": "ok" }
```

---

### Candidates List Dekho

```
GET /api/candidates
```
```json
[
  { "id": 0, "name": "Alice", "votes": 7 },
  { "id": 1, "name": "Bob",   "votes": 0 }
]
```

---

### Vote Karo

```
POST /api/vote
Content-Type: application/json

{
  "candidate_id": 0
}
```

---

### Results Dekho

```
GET /api/results
```
```json
{
  "status": "success",
  "results": [
    { "name": "Alice", "votes": 7 },
    { "name": "Bob",   "votes": 0 }
  ]
}
```

---

### Voter Register Karo

```
POST /api/register-voter
Content-Type: application/json

{
  "voter_address": "0xVoterEthAddress"
}
```

---

### Admin Routes

| Method | Endpoint | Kaam |
|--------|----------|------|
| POST | `/api/admin/add-candidate` | Naya candidate add karo (`{"name": "..."}`) |
| POST | `/api/admin/start-election` | Election shuru karo |
| POST | `/api/admin/end-election` | Election band karo |
| POST | `/api/admin/register-voter` | Voter register karo |

---

## Smart Contract — Functions

| Function | Access | Description |
|----------|--------|-------------|
| `addCandidate(name)` | Admin only | Candidate add karo (election shuru hone se pehle) |
| `startElection()` | Admin only | Election shuru karo |
| `endElection()` | Admin only | Election band karo |
| `resetElection()` | Admin only | Sab kuch reset karo (end ke baad) |
| `vote(candidateId)` | Registered voters | Vote cast karo |
| `getAllCandidates()` | Public | Saare candidates aur votes dekho |
| `getElectionState()` | Public | 0=NotStarted, 1=Ongoing, 2=Ended |

---

## Anomaly Detection

Voting logs analyze karne ke liye:

```bash
python backend/anomaly.py
```

Yeh script detect karti hai:
- **Multiple votes** — ek hi voter ne zyada baar vote kiya
- **Rapid voting** — 10 seconds ke andar dobara vote (suspicious activity)

Logs yahan store hote hain: `backend/logs/voting_logs.csv`

---

## Sample Data

**Voting Logs (`voting_logs.csv`):**
```
timestamp,voter,candidate
2025-12-20T12:23:14,0x5053...Aa0b,Alice
2025-12-20T12:26:35,0x5053...Aa0b,Alice
2025-12-20T12:26:48,0x5053...Aa0b,Alice
```

**Results (`storage/results.json`):**
```json
{
  "Alice": 7,
  "Bob": 0
}
```

---

## Election Flow (Step-by-Step)

```
1. Ganache Start
        ↓
2. Contract Deploy (deploy.py)
        ↓
3. .env mein CONTRACT_ADDRESS update karo
        ↓
4. Candidates Add karo (admin_add_candidates.py)
        ↓
5. Election Start karo (admin_start_election.py)
        ↓
6. Flask Server Chalao (python -m backend.api.app)
        ↓
7. POST /api/vote se vote karo
        ↓
8. GET /api/results se results dekho
        ↓
9. Election End karo (admin_end_election.py)
        ↓
10. Anomaly Check (python backend/anomaly.py)
```

---

## Common Errors

| Error | Solution |
|-------|----------|
| `Blockchain not connected` | Ganache chal raha hai? Port 8545 check karo |
| `CONTRACT_ADDRESS missing` | `.env` file mein address daalo |
| `Already voted` | Ek address se sirf ek baar vote ho sakta hai |
| `Election not active` | Pehle `startElection()` chalao |
| `Only admin` | Admin private key se transaction sign karo |

---

## Author

- GitHub: [riteshpatial](https://github.com/riteshpatial)
