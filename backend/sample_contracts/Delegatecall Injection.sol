// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Vulnerable to Delegatecall Attack
contract Proxy {
    address public implementation;

    function upgradeTo(address _impl) public {
        implementation = _impl;
    }

    fallback() external payable {
        (bool ok, ) = implementation.delegatecall(msg.data);
        require(ok);
    }
}