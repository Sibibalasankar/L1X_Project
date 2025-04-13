
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to Timestamp Manipulation
contract TimestampLottery {
    function bet() public view returns (bool) {
        return block.timestamp % 10 == 0; // Miner-influenced
    }
}