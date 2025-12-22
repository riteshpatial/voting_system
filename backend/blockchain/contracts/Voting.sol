// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    address public admin;

    enum ElectionState { NotStarted, Ongoing, Ended }
    ElectionState public electionState;

    struct Candidate {
        string name;
        uint votes;
    }

    Candidate[] public candidates;
    mapping(address => bool) public hasVoted;

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    constructor() {
        admin = msg.sender;
        electionState = ElectionState.NotStarted;
    }

    function addCandidate(string memory _name) public onlyAdmin {
        require(electionState == ElectionState.NotStarted, "Election started");
        candidates.push(Candidate(_name, 0));
    }

    function startElection() public onlyAdmin {
        require(electionState == ElectionState.NotStarted, "Already started");
        electionState = ElectionState.Ongoing;
    }

    function endElection() public onlyAdmin {
        require(electionState == ElectionState.Ongoing, "Not active");
        electionState = ElectionState.Ended;
    }

    // 🔥 NEW — allows admin to conduct fresh election
    function resetElection() public onlyAdmin {
        delete candidates;
        electionState = ElectionState.NotStarted;
    }

    function vote(uint candidateId) public {
        require(electionState == ElectionState.Ongoing, "Election not active");
        require(!hasVoted[msg.sender], "Already voted");
        require(candidateId < candidates.length, "Invalid candidate");

        candidates[candidateId].votes++;
        hasVoted[msg.sender] = true;
    }

    function getAllCandidates()
        public
        view
        returns (string[] memory names, uint[] memory votes)
    {
        names = new string[](candidates.length);
        votes = new uint[](candidates.length);

        for (uint i = 0; i < candidates.length; i++) {
            names[i] = candidates[i].name;
            votes[i] = candidates[i].votes;
        }
    }

    function getElectionState() public view returns (ElectionState) {
        return electionState;
    }
}
