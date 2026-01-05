// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    address public admin;

    enum ElectionState {
        NotStarted,
        Ongoing,
        Ended
    }

    ElectionState public electionState;

    struct Candidate {
        string name;
        uint256 votes;
    }

    Candidate[] public candidates;

    // voter => voted or not
    mapping(address => bool) public hasVoted;

    // 🔹 Track voters so we can reset mapping safely
    address[] private voterList;

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin");
        _;
    }

    constructor() {
        admin = msg.sender;
        electionState = ElectionState.NotStarted;
    }

    // =========================
    // ADMIN FUNCTIONS
    // =========================

    function addCandidate(string memory _name) public onlyAdmin {
        require(
            electionState == ElectionState.NotStarted,
            "Election already started"
        );

        candidates.push(Candidate(_name, 0));
    }

    function startElection() public onlyAdmin {
        require(
            electionState == ElectionState.NotStarted,
            "Election already started"
        );

        require(candidates.length > 0, "No candidates added");
        electionState = ElectionState.Ongoing;
    }

    function endElection() public onlyAdmin {
        require(
            electionState == ElectionState.Ongoing,
            "Election not active"
        );

        electionState = ElectionState.Ended;
    }

    // 🔥 FULL RESET — fresh election, no old data
    function resetElection() public onlyAdmin {
        require(
            electionState == ElectionState.Ended,
            "Election must end first"
        );

        // Reset candidates
        delete candidates;

        // Reset voter mapping safely
        for (uint256 i = 0; i < voterList.length; i++) {
            hasVoted[voterList[i]] = false;
        }
        delete voterList;

        electionState = ElectionState.NotStarted;
    }

    // =========================
    // VOTING
    // =========================

    function vote(uint256 candidateId) public {
        require(
            electionState == ElectionState.Ongoing,
            "Election not active"
        );

        require(!hasVoted[msg.sender], "Already voted");
        require(candidateId < candidates.length, "Invalid candidate");

        candidates[candidateId].votes += 1;
        hasVoted[msg.sender] = true;

        voterList.push(msg.sender);
    }

    // =========================
    // READ FUNCTIONS
    // =========================

    function getAllCandidates()
        public
        view
        returns (string[] memory names, uint256[] memory votes)
    {
        names = new string[](candidates.length);
        votes = new uint256[](candidates.length);

        for (uint256 i = 0; i < candidates.length; i++) {
            names[i] = candidates[i].name;
            votes[i] = candidates[i].votes;
        }
    }

    function getElectionState() public view returns (ElectionState) {
        return electionState;
    }
}
