import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';

/**JN
 * GenreByRegionChart Component
 * Task #27 - (P3) 3 - Create genre by region chart component
 * 
 * Displays a stacked bar chart showing genre distribution across US regions
 * (Northeast, Southeast, Midwest, West)
 */
const GenreByRegionChart = ({ apiUrl = 'http://localhost:8000' }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState('all');

  // US Regions for filter dropdown
  const regions = ['all', 'Northeast', 'Southeast', 'Midwest', 'West'];

  useEffect(() => {
    fetchGenreData();
  }, [selectedRegion]);

  const fetchGenreData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const endpoint = selectedRegion === 'all' 
        ? `${apiUrl}/api/genres/by-region`
        : `${apiUrl}/api/genres/by-region?region=${selectedRegion}`;
      
      const response = await axios.get(endpoint);
      setData(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching genre data:', err);
      setError(err.message || 'Failed to fetch genre data');
      setLoading(false);
    }
  };

  // Transform data for Plotly stacked bar chart
  const getPlotData = () => {
    if (!data || data.length === 0) return [];

    // Get unique genres and regions
    const genres = [...new Set(data.map(d => d.genre))];
    const regionsInData = [...new Set(data.map(d => d.region))];

    // Create a trace (series) for each genre
    return genres.map(genre => {
      const genreData = data.filter(d => d.genre === genre);
      
      return {
        x: regionsInData,
        y: genreData.map(d => d.stream_count),
        name: genre,
        type: 'bar',
        hovertemplate: '<b>%{x}</b><br>' +
                       genre + ': %{y:,} streams<br>' +
                       '<extra></extra>',
      };
    });
  };

  const layout = {
    title: {
      text: 'Genre Distribution by US Region',
      font: { size: 20, family: 'Arial, sans-serif' }
    },
    barmode: 'stack',
    xaxis: {
      title: 'Region',
      tickangle: -45,
    },
    yaxis: {
      title: 'Number of Streams',
      tickformat: ',',
    },
    hovermode: 'closest',
    showlegend: true,
    legend: {
      orientation: 'v',
      x: 1.02,
      y: 1,
      xanchor: 'left',
      yanchor: 'top',
    },
    margin: {
      l: 80,
      r: 150,
      t: 80,
      b: 100,
    },
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#f8f9fa',
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
  };

  if (loading) {
    return (
      <div className="genre-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <div className="spinner">Loading genre data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="genre-chart-container" style={{ padding: '20px' }}>
        <div className="error-message" style={{ 
          color: '#dc3545', 
          backgroundColor: '#f8d7da', 
          padding: '12px', 
          borderRadius: '4px',
          border: '1px solid #f5c6cb'
        }}>
          <strong>Error:</strong> {error}
          <button 
            onClick={fetchGenreData}
            style={{
              marginLeft: '10px',
              padding: '6px 12px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="genre-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <p style={{ color: '#6c757d' }}>No genre data available</p>
      </div>
    );
  }

  return (
    <div className="genre-chart-container" style={{ padding: '20px' }}>
      {/* Region Filter */}
      <div className="chart-controls" style={{ marginBottom: '20px' }}>
        <label htmlFor="region-filter" style={{ marginRight: '10px', fontWeight: 'bold' }}>
          Filter by Region:
        </label>
        <select
          id="region-filter"
          value={selectedRegion}
          onChange={(e) => setSelectedRegion(e.target.value)}
          style={{
            padding: '8px 12px',
            fontSize: '14px',
            borderRadius: '4px',
            border: '1px solid #ced4da',
            cursor: 'pointer'
          }}
        >
          {regions.map(region => (
            <option key={region} value={region}>
              {region === 'all' ? 'All Regions' : region}
            </option>
          ))}
        </select>
      </div>

      {/* Plotly Chart */}
      <Plot
        data={getPlotData()}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />

      {/* Data Summary */}
      <div className="chart-summary" style={{ 
        marginTop: '20px', 
        padding: '15px', 
        backgroundColor: '#f8f9fa',
        borderRadius: '4px',
        fontSize: '14px',
        color: '#495057'
      }}>
        <strong>Total Streams:</strong> {data.reduce((sum, d) => sum + d.stream_count, 0).toLocaleString()}
        <span style={{ marginLeft: '20px' }}>
          <strong>Genres:</strong> {[...new Set(data.map(d => d.genre))].length}
        </span>
        <span style={{ marginLeft: '20px' }}>
          <strong>Regions:</strong> {[...new Set(data.map(d => d.region))].length}
        </span>
      </div>
    </div>
  );
};

export default GenreByRegionChart;
