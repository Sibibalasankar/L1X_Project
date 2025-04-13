from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model and vectorizer
model = joblib.load('./models/vulnerability_model.pkl')
vectorizer = joblib.load('./models/tfidf_vectorizer.pkl')

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.json
    print("Received Data:", data)  # Debugging: Print the received data
    
    code = data.get('code', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    # Check if the input code is too short (e.g., single characters)
    if len(code) < 20:  # Adjust the threshold based on your needs
        return jsonify({'error': 'Input code is too short to analyze'}), 400

    # Input Validation: Check if the code appears to be a smart contract
    def is_possible_smart_contract(code):
        keywords = ['pragma', 'contract', 'address', 'uint', 'require']
        result = any(keyword in code for keyword in keywords)
        print("Is possible smart contract:", result)  # Debugging: Print validation result
        return result

    if not is_possible_smart_contract(code):
        return jsonify({'error': 'Input does not appear to be a smart contract'}), 400

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
        
        return jsonify({
            'prediction': prediction,
            'confidence_scores': confidence_scores,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
