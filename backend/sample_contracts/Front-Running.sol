
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to Front-Running
contract Auction {
    uint public highestBid;
    address public highestBidder;

    function bid() public payable {
        require(msg.value > highestBid);
        highestBid = msg.value;
        highestBidder = msg.sender; // Transparent state change
    }
}