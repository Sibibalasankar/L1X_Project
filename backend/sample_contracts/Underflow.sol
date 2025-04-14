// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to Integer Overflow
contract Overflow {
    uint8 public count = 255;

    function increment() public {
        count += 1; // Will overflow to 0
    }
}