
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to Uninitialized Storage
contract StorageBug {
    uint public value; // Uninitialized

    function set(uint x) public {
        value = x; // Writes to slot 0 by default
    }
}