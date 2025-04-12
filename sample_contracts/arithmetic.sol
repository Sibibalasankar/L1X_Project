// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Arithmetic {
    function divide(uint a, uint b) public pure returns (uint) {
        // Vulnerability: Division by zero
        require(b != 0, "Cannot divide by zero");
        return a / b;
    }
}
