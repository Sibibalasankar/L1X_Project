import { useState, useEffect } from 'react';
import axios from 'axios';
import { FiCode, FiAlertTriangle, FiSearch, FiSun, FiMoon } from 'react-icons/fi';
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

  const analyzeCode = async () => {
    if (!code.trim()) {
      setError('Please enter Solidity code to analyze');
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

  return (
    <div className={`analyzer-container ${darkMode ? 'dark-mode' : ''}`}>
      <header className="analyzer-header">
        <div className="header-content">
          <h1>Solidity Vulnerability Analyzer</h1>
          <p className="subtitle">
            Paste your Solidity contract below to detect potential vulnerabilities 
          </p>
        </div>
        <button 
          className="dark-mode-toggle"
          onClick={toggleDarkMode}
          aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? <FiSun className="toggle-icon" /> : <FiMoon className="toggle-icon" />}
          <span>{darkMode ? 'Light Mode' : 'Dark Mode'}</span>
        </button>
      </header>

      <div className="content-grid">
        <div className="code-section">
          <div className="section-header">
            <FiCode className="icon" />
            <h2>Solidity Code Input</h2>
          </div>
          <textarea
            className="code-input"
            placeholder="Paste your Solidity contract here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          <button 
            className="analyze-btn" 
            onClick={analyzeCode}
            disabled={isAnalyzing}
          >
            <FiSearch className="btn-icon" />
            {isAnalyzing ? 'Analyzing...' : 'Analyze Contract'}
          </button>
        </div>

        <div className="results-section">
          <div className="section-header">
            <FiAlertTriangle className="icon" />
            <h2>Analysis Results</h2>
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {isAnalyzing ? (
            <div className="loading-state">
              <div className="spinner"></div>
              <p>Analyzing contract...</p>
            </div>
          ) : results ? (
            <div className="results-content">
              <div className="prediction-section">
                <h3>Predicted Vulnerability</h3>
                <div className={`prediction-tag ${
                  results.prediction === 'Safe' ? 'safe' : 'vulnerable'
                }`}>
                  {results.prediction}
                  <span className="confidence-percentage">
                    ({Math.max(...Object.values(results.confidence_scores)) * 100}% confidence)
                  </span>
                </div>
              </div>

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
                        <div 
                          className="score-bar"
                          style={{ width: `${score * 100}%` }}
                        ></div>
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
        Solidity Vulnerability Analyzer - Powered by Audit smart AI
      </footer>
    </div>
  );
}

export default App;