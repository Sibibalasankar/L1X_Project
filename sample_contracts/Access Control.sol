// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Missing Access Control
contract Adminless {
    address public admin;
    uint public secret;

    function setSecret(uint _secret) public {
        secret = _secret; // No admin check
    }
}