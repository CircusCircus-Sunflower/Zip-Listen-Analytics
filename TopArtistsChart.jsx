import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';

/**
 * TopArtistsChart Component
 * Task #29 - (P3) 5 - Create top artists list component
 * 
 * Displays a horizontal bar chart showing the top artists by total stream count
 */
const TopArtistsChart = ({ apiUrl = 'http://localhost:8000', limit = 10 }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [artistLimit, setArtistLimit] = useState(limit);

  useEffect(() => {
    fetchTopArtists();
  }, [artistLimit]);

  const fetchTopArtists = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${apiUrl}/api/artists/top?limit=${artistLimit}`);
      setData(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching top artists:', err);
      setError(err.message || 'Failed to fetch top artists');
      setLoading(false);
    }
  };

  // Transform data for Plotly horizontal bar chart
  const getPlotData = () => {
    if (!data || data.length === 0) return [];

    // Sort by stream count descending (API should already do this, but ensure it)
    const sortedData = [...data].sort((a, b) => b.stream_count - a.stream_count);

    return [{
      x: sortedData.map(d => d.stream_count),
      y: sortedData.map(d => d.artist),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: sortedData.map((_, index) => {
          // Gradient from purple to blue based on rank
          const colors = [
            '#8b5cf6', '#7c3aed', '#6d28d9', '#5b21b6', 
            '#4c1d95', '#3b82f6', '#2563eb', '#1d4ed8',
            '#1e40af', '#1e3a8a'
          ];
          return colors[index % colors.length];
        }),
        line: {
          color: 'rgba(255, 255, 255, 0.3)',
          width: 1
        }
      },
      text: sortedData.map(d => `${d.stream_count.toLocaleString()} streams`),
      textposition: 'outside',
      textfont: {
        size: 11,
        color: '#374151'
      },
      hovertemplate: '<b>%{y}</b><br>' +
                     'Streams: %{x:,}<br>' +
                     'Rank: %{customdata}<br>' +
                     '<extra></extra>',
      customdata: sortedData.map(d => d.rank || '#' + (sortedData.indexOf(d) + 1))
    }];
  };

  const layout = {
    title: {
      text: `Top ${artistLimit} Most-Streamed Artists`,
      font: { size: 20, family: 'Arial, sans-serif' }
    },
    xaxis: {
      title: 'Total Streams',
      tickformat: ',',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)'
    },
    yaxis: {
      title: '',
      autorange: 'reversed', // Top artist at the top
      tickfont: {
        size: 12
      }
    },
    margin: {
      l: 150, // Space for artist names
      r: 100,
      t: 80,
      b: 60,
    },
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#f8f9fa',
    showlegend: false,
    hovermode: 'closest',
    height: Math.max(400, data.length * 35), // Dynamic height based on number of artists
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
  };

  if (loading) {
    return (
      <div className="top-artists-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <div className="spinner">Loading top artists...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="top-artists-chart-container" style={{ padding: '20px' }}>
        <div className="error-message" style={{ 
          color: '#dc3545', 
          backgroundColor: '#f8d7da', 
          padding: '12px', 
          borderRadius: '4px',
          border: '1px solid #f5c6cb'
        }}>
          <strong>Error:</strong> {error}
          <button 
            onClick={fetchTopArtists}
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
      <div className="top-artists-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <p style={{ color: '#6c757d' }}>No artist data available</p>
      </div>
    );
  }

  const totalStreams = data.reduce((sum, artist) => sum + artist.stream_count, 0);
  const avgStreams = Math.round(totalStreams / data.length);

  return (
    <div className="top-artists-chart-container" style={{ padding: '20px' }}>
      {/* Limit Selector */}
      <div className="chart-controls" style={{ 
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <label htmlFor="artist-limit" style={{ marginRight: '10px', fontWeight: 'bold' }}>
            Show Top:
          </label>
          <select
            id="artist-limit"
            value={artistLimit}
            onChange={(e) => setArtistLimit(parseInt(e.target.value))}
            style={{
              padding: '8px 12px',
              fontSize: '14px',
              borderRadius: '4px',
              border: '1px solid #ced4da',
              cursor: 'pointer'
            }}
          >
            <option value="5">Top 5</option>
            <option value="10">Top 10</option>
            <option value="15">Top 15</option>
            <option value="20">Top 20</option>
            <option value="25">Top 25</option>
            <option value="50">Top 50</option>
          </select>
        </div>
        
        <div style={{ fontSize: '14px', color: '#6c757d' }}>
          Total Artists: <strong>{data.length}</strong>
        </div>
      </div>

      {/* Plotly Chart */}
      <Plot
        data={getPlotData()}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />

      {/* Summary Statistics */}
      <div className="chart-summary" style={{ 
        marginTop: '20px', 
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '15px'
      }}>
        <div style={{
          padding: '15px',
          backgroundColor: '#e0e7ff',
          borderRadius: '4px',
          border: '1px solid #c7d2fe'
        }}>
          <div style={{ fontSize: '12px', color: '#3730a3', marginBottom: '5px' }}>
            #1 ARTIST
          </div>
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#3730a3' }}>
            {data[0]?.artist}
          </div>
          <div style={{ fontSize: '12px', color: '#4338ca', marginTop: '3px' }}>
            {data[0]?.stream_count.toLocaleString()} streams
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#dbeafe',
          borderRadius: '4px',
          border: '1px solid #bfdbfe'
        }}>
          <div style={{ fontSize: '12px', color: '#1e40af', marginBottom: '5px' }}>
            TOTAL STREAMS (TOP {artistLimit})
          </div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#1e40af' }}>
            {totalStreams.toLocaleString()}
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#f0fdf4',
          borderRadius: '4px',
          border: '1px solid #bbf7d0'
        }}>
          <div style={{ fontSize: '12px', color: '#15803d', marginBottom: '5px' }}>
            AVERAGE STREAMS
          </div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#15803d' }}>
            {avgStreams.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Top 3 Highlight */}
      <div style={{
        marginTop: '20px',
        padding: '15px',
        backgroundColor: '#fef3c7',
        borderRadius: '4px',
        border: '1px solid #fde68a'
      }}>
        <strong style={{ color: '#92400e' }}>🏆 Top 3 Artists:</strong>
        <ol style={{ margin: '10px 0 0 20px', color: '#78350f' }}>
          {data.slice(0, 3).map((artist, index) => (
            <li key={index} style={{ marginBottom: '5px' }}>
              <strong>{artist.artist}</strong> - {artist.stream_count.toLocaleString()} streams
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
};

export default TopArtistsChart;
