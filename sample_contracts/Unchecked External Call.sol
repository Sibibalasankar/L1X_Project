
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to Unchecked Call
contract BlindTransfer {
    function sendEther(address payable recipient) public payable {
        recipient.send(msg.value); // No check for success
    }
}