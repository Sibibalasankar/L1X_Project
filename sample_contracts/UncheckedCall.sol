// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UncheckedCall {
    function sendTo(address payable recipient) public payable {
        recipient.call{value: msg.value}(""); // No check on success
    }
}
