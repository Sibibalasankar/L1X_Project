
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
// Vulnerable to Arbitrary Jump
contract Jumper {
    function execute(bytes memory code) public {
        assembly {
            jump(add(code, 0x20))
        }
    }
}