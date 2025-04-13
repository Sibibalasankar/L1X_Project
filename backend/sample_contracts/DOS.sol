
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to DoS via Block Gas Limit
contract GasGuzzler {
    address[] public users;

    function addUsers() public {
        for (uint i = 0; i < 1000; i++) {
            users.push(msg.sender); // May exhaust gas
        }
    }
}