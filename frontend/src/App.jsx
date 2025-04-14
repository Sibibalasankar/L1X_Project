import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  FiCode,
  FiAlertTriangle,
  FiSearch,
  FiSun,
  FiMoon,
  FiUpload
} from 'react-icons/fi';
import { FaWallet } from 'react-icons/fa';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(() => {
    const savedMode = localStorage.getItem('darkMode');
    return savedMode ? JSON.parse(savedMode) : window.matchMedia('(prefers-color-scheme: dark)').matches;
  });
  const [walletConnected, setWalletConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState('');
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
      localStorage.setItem('darkMode', 'true');
    } else {
      document.body.classList.remove('dark-mode');
      localStorage.setItem('darkMode', 'false');
    }
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const connectWallet = async () => {
    try {
      const mockAddress = '0x71C7656EC7ab88b098defB751B7401B5f6d8976F';
      setWalletConnected(true);
      setWalletAddress(mockAddress);
    } catch (err) {
      setError('Failed to connect wallet');
    }
  };

  const disconnectWallet = () => {
    setWalletConnected(false);
    setWalletAddress('');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.sol')) {
      setError('Please upload a Solidity file (.sol)');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      setCode(e.target.result);
      setError(null);
    };
    reader.onerror = () => {
      setError('Error reading file');
    };
    reader.readAsText(file);
  };

  const triggerFileInput = () => {
    fileInputRef.current.click();
  };

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError('Please enter Solidity code to analyze or upload a .sol file');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/analyze', {
        code: code
      });
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred during analysis');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const vulnerabilityExplanations = {
    Reentrancy: "This score reflects detected patterns of unguarded external calls or recursive function behavior.",
    IntegerOverflow: "High score due to absence of SafeMath or input validation.",
    UncheckedCall: "Score is based on the use of low-level calls without return value handling.",
  };

  const autoResizeTextarea = (e) => {
    const textarea = e.target;
    textarea.style.height = 'auto';
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  return (
    <div className={`analyzer-container ${darkMode ? 'dark-mode' : ''}`}>
      <header className="analyzer-header">
        <div className="header-content">
          <h1>Smart Contract Audit</h1>
          <p className="subtitle">
            Paste your Solidity contract below or upload a .sol file to detect potential vulnerabilities
          </p>
        </div>
        <div className="header-actions">
          <button
            className={`wallet-btn ${walletConnected ? 'connected' : ''}`}
            onClick={walletConnected ? disconnectWallet : connectWallet}
          >
            <FaWallet className="btn-icon" />
            <span>
              {walletConnected
                ? `${walletAddress.substring(0, 6)}...${walletAddress.substring(walletAddress.length - 4)}`
                : 'Connect Wallet'}
            </span>
          </button>
          <button className="dark-mode-toggle" onClick={toggleDarkMode}>
            {darkMode ? <FiSun className="toggle-icon" /> : <FiMoon className="toggle-icon" />}
          </button>
        </div>
      </header>

      <div className="content-grid">
        <div className="code-section">
          <div className="section-header">
            <FiCode className="icon" />
            <h2>Solidity Code Input</h2>
          </div>
          <textarea
            className="code-input"
            placeholder="Paste your Solidity contract here or upload a .sol file..."
            value={code}
            onChange={(e) => {
              setCode(e.target.value);
              autoResizeTextarea(e);
            }}
            ref={fileInputRef}
          />
          <div className="input-actions">
            <button className="upload-btn" onClick={triggerFileInput}>
              <FiUpload className="btn-icon" />
              Upload .sol File
            </button>
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              accept=".sol"
              style={{ display: 'none' }}
            />
            <button className="analyze-btn" onClick={analyzeCode} disabled={isAnalyzing}>
              <FiSearch className="btn-icon" />
              {isAnalyzing ? 'Analyzing...' : 'Analyze Contract'}
            </button>
          </div>
        </div>

        <div className="results-section">
          <div className="section-header">
            <FiAlertTriangle className="icon" />
            <h2>Analysis Results</h2>
          </div>

          {error && <div className="error-message">{error}</div>}

          {isAnalyzing ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Analyzing contract...</p>
            </div>
          ) : results ? (
            <div className="results-content">
              <div className="prediction-section">
                <h3>Predicted Vulnerability</h3>
                <div className={`prediction-tag ${results.prediction === 'Safe' ? 'safe' : 'vulnerable'}`}>
                  {results.prediction}
                  <span className="confidence-percentage">
                    ({Math.max(...Object.values(results.confidence_scores)) * 100}% confidence)
                  </span>
                </div>
              </div>

              {results.vulnerability_details && (
                <div className="vulnerability-details">
                  <h3>🛡️ Vulnerability Details</h3>
                  <div className="detail-item">
                    <strong>Severity:</strong> {results.vulnerability_details.severity}
                  </div>
                  <div className="detail-item">
                    <strong>CWE ID:</strong> {results.vulnerability_details.cwe_id}
                  </div>
                  <div className="detail-item">
                    <strong>Description:</strong>
                    <p>{results.vulnerability_details.description}</p>
                  </div>
                  <div className="detail-items">
                    <strong>Secure Example:</strong>
                    <pre className="secure-example">{results.vulnerability_details.secure_example}</pre>
                  </div>
                </div>
              )}

              <div className="confidence-section">
                <h3>Confidence Scores</h3>
                <div className="confidence-grid">
                  {Object.entries(results.confidence_scores).map(([vuln, score]) => (
                    <div key={vuln} className="confidence-item">
                      <div className="vulnerability-name">
                        {vuln}
                        <span className="percentage-badge">{(score * 100).toFixed(1)}%</span>
                      </div>
                      <div className="score-bar-container">
                        <div className="score-bar" style={{ width: `${score * 100}%` }}></div>
                        <div className="tooltip-text">
                          {vulnerabilityExplanations[vuln] || `Details about ${vuln}`}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <p>Results will appear here after analysis</p>
            </div>
          )}
        </div>
      </div>

      <footer className="analyzer-footer">
        Solidity Vulnerability Analyzer - Powered by Audit Smart AI
      </footer>
    </div>
  );
}

export default App;
