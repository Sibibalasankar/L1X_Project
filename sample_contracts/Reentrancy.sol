// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReentrancyVulnerability {
    mapping(address => uint256) public balances;

    // Deposit function allows users to send funds
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // Withdraw function is vulnerable to reentrancy
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // Transfer funds before updating the balance (vulnerable to reentrancy attack)
        msg.sender.transfer(amount);
        
        // Update balance
        balances[msg.sender] -= amount;
    }
}
