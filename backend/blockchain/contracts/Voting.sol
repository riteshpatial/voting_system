// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Voting {
    address public admin;

    enum ElectionState { NotStarted, Active, Ended }
    ElectionState public electionState;

    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }

    mapping(uint => Candidate) private candidates;
    uint private candidatesCount;

    mapping(address => bool) public hasVoted;

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    constructor() {
        admin = msg.sender;
        electionState = ElectionState.NotStarted;
    }

    function addCandidate(string memory _name) external onlyAdmin {
        require(electionState == ElectionState.NotStarted, "Election started");
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, _name, 0);
    }

    function startElection() external onlyAdmin {
        require(candidatesCount > 0, "No candidates");
        electionState = ElectionState.Active;
    }

    function vote(uint _id) external {
        require(electionState == ElectionState.Active, "Not active");
        require(!hasVoted[msg.sender], "Already voted");
        require(_id > 0 && _id <= candidatesCount, "Invalid candidate");

        hasVoted[msg.sender] = true;
        candidates[_id].voteCount++;
    }

    function endElection() external onlyAdmin {
        require(electionState == ElectionState.Active, "Not active");
        electionState = ElectionState.Ended;
    }

    function getCandidatesCount() external view returns (uint) {
        return candidatesCount;
    }

    // ✅ FIXED FUNCTION
    function getAllCandidates()
        external
        view
        returns (string[] memory names, uint[] memory votes)
    {
        require(electionState == ElectionState.Ended, "Election not ended");

        names = new string[](candidatesCount);
        votes = new uint[](candidatesCount);

        for (uint i = 1; i <= candidatesCount; i++) {
            names[i - 1] = candidates[i].name;
            votes[i - 1] = candidates[i].voteCount;
        }
    }
}
