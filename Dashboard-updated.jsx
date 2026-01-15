import React, { useState } from 'react';
import GenreByRegionChart from './GenreByRegionChart';
import SubscriberBreakdownChart from './SubscriberBreakdownChart';
import TopArtistsChart from './TopArtistsChart';
import RisingArtistsChart from './RisingArtistsChart';
import './Dashboard.css';

/**
 * Main Dashboard Component
 * Integrates all analytics visualizations for Zip Listen executives
 * 
 * Tasks included:
 * - #26: Dashboard layout component
 * - #27: Genre by region chart component  
 * - #28: Subscriber breakdown chart component
 */
const Dashboard = () => {
  const [apiUrl] = useState(process.env.REACT_APP_API_URL || 'http://localhost:8000');
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🎵 Zip Listen Analytics</h1>
          <p className="subtitle">Executive Dashboard - Music Streaming Insights</p>
        </div>
        <div className="header-actions">
          <button className="refresh-btn" onClick={() => window.location.reload()}>
            🔄 Refresh Data
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="dashboard-nav">
        <button 
          className={`nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button 
          className={`nav-tab ${activeTab === 'genres' ? 'active' : ''}`}
          onClick={() => setActiveTab('genres')}
        >
          🎸 Genres
        </button>
        <button 
          className={`nav-tab ${activeTab === 'subscribers' ? 'active' : ''}`}
          onClick={() => setActiveTab('subscribers')}
        >
          👥 Subscribers
        </button>
        <button 
          className={`nav-tab ${activeTab === 'artists' ? 'active' : ''}`}
          onClick={() => setActiveTab('artists')}
        >
          ⭐ Artists
        </button>
      </nav>

      {/* Main Content */}
      <main className="dashboard-content">
        {/* Overview Tab - Shows all charts */}
        {activeTab === 'overview' && (
          <div className="overview-grid">
            <section className="chart-card">
              <GenreByRegionChart apiUrl={apiUrl} />
            </section>
            
            <section className="chart-card">
              <SubscriberBreakdownChart apiUrl={apiUrl} />
            </section>

            <section className="chart-card">
              <TopArtistsChart apiUrl={apiUrl} limit={10} />
            </section>

            <section className="chart-card">
              <RisingArtistsChart apiUrl={apiUrl} limit={10} />
            </section>
          </div>
        )}

        {/* Genres Tab - Full width genre chart */}
        {activeTab === 'genres' && (
          <div className="single-chart-view">
            <section className="chart-card full-width">
              <GenreByRegionChart apiUrl={apiUrl} />
            </section>
          </div>
        )}

        {/* Subscribers Tab - Full width subscriber chart */}
        {activeTab === 'subscribers' && (
          <div className="single-chart-view">
            <section className="chart-card full-width">
              <SubscriberBreakdownChart apiUrl={apiUrl} />
            </section>
          </div>
        )}

        {/* Artists Tab - Now with actual components */}
        {activeTab === 'artists' && (
          <div className="artists-grid">
            <section className="chart-card">
              <TopArtistsChart apiUrl={apiUrl} limit={15} />
            </section>

            <section className="chart-card">
              <RisingArtistsChart apiUrl={apiUrl} limit={15} />
            </section>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="dashboard-footer">
        <p>Zip Listen Analytics Platform | Built with React, FastAPI & PostgreSQL</p>
        <p style={{ fontSize: '12px', color: '#6c757d' }}>
          API Status: <span style={{ color: '#28a745' }}>● Connected</span>
        </p>
      </footer>
    </div>
  );
};

export default Dashboard;
