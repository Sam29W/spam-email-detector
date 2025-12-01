import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EmailInput from './components/EmailInput';
import ResultsDisplay from './components/ResultsDisplay';
import BatchProcessor from './components/BatchProcessor';
import Analytics from './components/Analytics';
import './styles/App.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [activeTab, setActiveTab] = useState('detector');
  const [darkMode, setDarkMode] = useState(false);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  return (
    <div className={`app ${darkMode ? 'dark' : 'light'}`}>
      <nav className="navbar">
        <div className="nav-container">
          <h1 className="app-title">Spam Email Detector</h1>
          <button
            className="theme-toggle"
            onClick={() => setDarkMode(!darkMode)}
            title="Toggle dark mode"
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </nav>

      <div className="tabs-container">
        <button
          className={`tab-button ${activeTab === 'detector' ? 'active' : ''}`}
          onClick={() => setActiveTab('detector')}
        >
          Single Detection
        </button>
        <button
          className={`tab-button ${activeTab === 'batch' ? 'active' : ''}`}
          onClick={() => setActiveTab('batch')}
        >
          Batch Process
        </button>
        <button
          className={`tab-button ${activeTab === 'analytics' ? 'active' : ''}`}
          onClick={() => setActiveTab('analytics')}
        >
          Analytics
        </button>
      </div>

      <div className="main-content">
        {activeTab === 'detector' && <EmailInput onAnalyzed={fetchStats} />}
        {activeTab === 'batch' && <BatchProcessor onAnalyzed={fetchStats} />}
        {activeTab === 'analytics' && <Analytics stats={stats} />}
      </div>

      {stats && (
        <footer className="stats-footer">
          <div className="stats-info">
            <span>Total Analyzed: {stats.total_emails_analyzed}</span>
            <span>Spam: {stats.spam_detected}</span>
            <span>Legitimate: {stats.legitimate_emails}</span>
            <span>Accuracy: {(stats.accuracy_rate * 100).toFixed(1)}%</span>
          </div>
        </footer>
      )}
    </div>
  );
}

export default App;
