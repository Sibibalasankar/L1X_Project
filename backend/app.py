from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and vectorizer
model = joblib.load('./models/vulnerability_model_20250413-191529.pkl')
vectorizer = joblib.load('./models/tfidf_vectorizer_20250413-191529.pkl')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    print("Received Data:", data)
    
    code = data.get('code', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    if len(code) < 20:
        return jsonify({'error': 'Input code is too short to analyze'}), 400
    
    def is_possible_smart_contract(code):
        keywords = ['pragma', 'contract', 'address', 'uint', 'require']
        result = any(keyword in code for keyword in keywords)
        print("Is possible smart contract:", result)
        return result

    if not is_possible_smart_contract(code):
        return jsonify({'error': 'Input does not appear to be a smart contract'}), 400

    # Dictionary mapping vulnerabilities to their details
    vulnerability_details_mapping = {
    'Reentrancy': {
        'severity': 'High',
        'cwe_id': 'CWE-841',
        'description': 'External call before state update',
        'secure_example': 'contract Secure { mapping(address => uint) balances; function withdraw() public { uint amount = balances[msg.sender]; balances[msg.sender] = 0; (bool success, ) = msg.sender.call{value: amount}(""); require(success); }}',
    },
    'Integer Overflow': {
        'severity': 'Medium',
        'cwe_id': 'CWE-190',
        'description': 'Unchecked increment',
        'secure_example': 'contract SafeCounter { uint8 public count = 255; function increment() public { require(count < type(uint8).max); count += 1; }}',
    },
    'Unchecked External Calls': {
        'severity': 'Medium',
        'cwe_id': 'CWE-476',
        'description': 'No success check',
        'secure_example': 'contract SafeTransfer { function transfer(address payable dest, uint amount) public { (bool success, ) = dest.call{value: amount}(""); require(success); }}',
    },
    'Timestamp Dependence': {
        'severity': 'Low',
        'cwe_id': 'CWE-829',
        'description': 'Block timestamp reliance',
        'secure_example': 'contract SecureGame { function play() public { require(uint(keccak256(abi.encodePacked(blockhash(block.number-1))) % 2 == 0); }}',
    },
    'Denial of Service': {
        'severity': 'High',
        'cwe_id': 'CWE-400',
        'description': 'Unbounded loop',
        'secure_example': 'contract SafeRefund { address[] recipients; function refundAll() public { uint gasLimit = gasleft() / recipients.length; for (uint i = 0; i < recipients.length; i++) { (bool success, ) = payable(recipients[i]).call{value: 1 ether, gas: gasLimit}(""); require(success); }}}',
    },
    'Front-Running': {
        'severity': 'Medium',
        'cwe_id': 'CWE-300',
        'description': 'Transparent bidding',
        'secure_example': 'contract CommitAuction { mapping(address => bytes32) bids; function commitBid(bytes32 hash) public { bids[msg.sender] = hash; } function revealBid(uint value, bytes32 secret) public { require(keccak256(abi.encodePacked(value, secret)) == bids[msg.sender]); }}',
    },
    # Add other vulnerabilities following the same pattern
    }

    try:
        # Vectorize the code
        code_vec = vectorizer.transform([code])
        
        # Get prediction and confidence scores
        prediction = model.predict(code_vec)[0]
        probabilities = model.predict_proba(code_vec)[0]
        
        # Prepare confidence scores
        confidence_scores = {
            model.classes_[i]: float(prob)  # Convert numpy float to Python float
            for i, prob in enumerate(probabilities)
        }

        # Get the corresponding vulnerability details
        vulnerability_details = vulnerability_details_mapping.get(prediction, {
            'severity': 'Unknown',
            'cwe_id': 'N/A',
            'description': 'No description available for this vulnerability.',
            'secure_example': 'No secure example available.',
        })

        return jsonify({
            'prediction': prediction,
            'confidence_scores': confidence_scores,
            'vulnerability_details': vulnerability_details,  # Include dynamic details
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
