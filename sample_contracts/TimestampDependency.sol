// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lottery {
    address public winner;

    function play() public {
        if (block.timestamp % 2 == 0) {
            winner = msg.sender;
        }
    }
}
