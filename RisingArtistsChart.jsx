import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';

/**JN
 * RisingArtistsChart Component
 * Task #30 - (P3) 6 - Create rising artists component
 * 
 * Displays artists with the highest growth rate, identifying trending talent
 */
const RisingArtistsChart = ({ apiUrl = 'http://localhost:8000', limit = 10 }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [artistLimit, setArtistLimit] = useState(limit);

  useEffect(() => {
    fetchRisingArtists();
  }, [artistLimit]);

  const fetchRisingArtists = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${apiUrl}/api/artists/rising?limit=${artistLimit}`);
      setData(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching rising artists:', err);
      setError(err.message || 'Failed to fetch rising artists');
      setLoading(false);
    }
  };

  // Transform data for Plotly horizontal bar chart with growth indicators
  const getPlotData = () => {
    if (!data || data.length === 0) return [];

    // Sort by growth rate descending
    const sortedData = [...data].sort((a, b) => b.growth_rate - a.growth_rate);

    return [{
      x: sortedData.map(d => d.growth_rate),
      y: sortedData.map(d => d.artist),
      type: 'bar',
      orientation: 'h',
      marker: {
        color: sortedData.map(d => {
          // Color intensity based on growth rate
          if (d.growth_rate >= 200) return '#dc2626'; // Red for explosive growth
          if (d.growth_rate >= 150) return '#ea580c'; // Orange
          if (d.growth_rate >= 100) return '#f59e0b'; // Amber
          if (d.growth_rate >= 50) return '#84cc16'; // Lime
          return '#22c55e'; // Green
        }),
        line: {
          color: 'rgba(255, 255, 255, 0.3)',
          width: 1
        }
      },
      text: sortedData.map(d => `+${d.growth_rate.toFixed(1)}%`),
      textposition: 'outside',
      textfont: {
        size: 11,
        color: '#374151',
        weight: 'bold'
      },
      hovertemplate: '<b>%{y}</b><br>' +
                     'Growth Rate: +%{x:.1f}%<br>' +
                     'Current Streams: %{customdata.current:,}<br>' +
                     'Previous Streams: %{customdata.previous:,}<br>' +
                     '<extra></extra>',
      customdata: sortedData.map(d => ({
        current: d.current_streams,
        previous: d.previous_streams
      }))
    }];
  };

  const layout = {
    title: {
      text: `Top ${artistLimit} Rising Artists by Growth Rate`,
      font: { size: 20, family: 'Arial, sans-serif' }
    },
    xaxis: {
      title: 'Growth Rate (%)',
      showgrid: true,
      gridcolor: 'rgba(0,0,0,0.1)',
      zeroline: false
    },
    yaxis: {
      title: '',
      autorange: 'reversed',
      tickfont: {
        size: 12
      }
    },
    margin: {
      l: 150,
      r: 100,
      t: 80,
      b: 60,
    },
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#f8f9fa',
    showlegend: false,
    hovermode: 'closest',
    height: Math.max(400, data.length * 35),
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
  };

  if (loading) {
    return (
      <div className="rising-artists-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <div className="spinner">Loading rising artists...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rising-artists-chart-container" style={{ padding: '20px' }}>
        <div className="error-message" style={{ 
          color: '#dc3545', 
          backgroundColor: '#f8d7da', 
          padding: '12px', 
          borderRadius: '4px',
          border: '1px solid #f5c6cb'
        }}>
          <strong>Error:</strong> {error}
          <button 
            onClick={fetchRisingArtists}
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
      <div className="rising-artists-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <p style={{ color: '#6c757d' }}>No rising artist data available</p>
      </div>
    );
  }

  const avgGrowth = data.reduce((sum, artist) => sum + artist.growth_rate, 0) / data.length;
  const topGrowth = data[0]?.growth_rate || 0;

  return (
    <div className="rising-artists-chart-container" style={{ padding: '20px' }}>
      {/* Limit Selector */}
      <div className="chart-controls" style={{ 
        marginBottom: '20px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <div>
          <label htmlFor="rising-limit" style={{ marginRight: '10px', fontWeight: 'bold' }}>
            Show Top:
          </label>
          <select
            id="rising-limit"
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
          Rising Stars: <strong>{data.length}</strong>
        </div>
      </div>

      {/* Growth Legend */}
      <div style={{
        marginBottom: '15px',
        padding: '10px',
        backgroundColor: '#f3f4f6',
        borderRadius: '4px',
        fontSize: '12px',
        display: 'flex',
        gap: '15px',
        flexWrap: 'wrap'
      }}>
        <span><span style={{display: 'inline-block', width: '15px', height: '15px', backgroundColor: '#dc2626', marginRight: '5px'}}></span>200%+ (Explosive)</span>
        <span><span style={{display: 'inline-block', width: '15px', height: '15px', backgroundColor: '#ea580c', marginRight: '5px'}}></span>150-200% (Very High)</span>
        <span><span style={{display: 'inline-block', width: '15px', height: '15px', backgroundColor: '#f59e0b', marginRight: '5px'}}></span>100-150% (High)</span>
        <span><span style={{display: 'inline-block', width: '15px', height: '15px', backgroundColor: '#84cc16', marginRight: '5px'}}></span>50-100% (Moderate)</span>
        <span><span style={{display: 'inline-block', width: '15px', height: '15px', backgroundColor: '#22c55e', marginRight: '5px'}}></span>&lt;50% (Growing)</span>
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
          backgroundColor: '#fee2e2',
          borderRadius: '4px',
          border: '1px solid #fecaca'
        }}>
          <div style={{ fontSize: '12px', color: '#991b1b', marginBottom: '5px' }}>
            🚀 FASTEST GROWING
          </div>
          <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#991b1b' }}>
            {data[0]?.artist}
          </div>
          <div style={{ fontSize: '14px', color: '#b91c1c', marginTop: '3px' }}>
            +{data[0]?.growth_rate.toFixed(1)}% growth
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#fef3c7',
          borderRadius: '4px',
          border: '1px solid #fde68a'
        }}>
          <div style={{ fontSize: '12px', color: '#92400e', marginBottom: '5px' }}>
            AVERAGE GROWTH RATE
          </div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#92400e' }}>
            +{avgGrowth.toFixed(1)}%
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#dcfce7',
          borderRadius: '4px',
          border: '1px solid '#bbf7d0'
        }}>
          <div style={{ fontSize: '12px', color: '#166534', marginBottom: '5px' }}>
            ARTISTS TRACKED
          </div>
          <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#166534' }}>
            {data.length}
          </div>
        </div>
      </div>

      {/* Top 3 Rising Stars Highlight */}
      <div style={{
        marginTop: '20px',
        padding: '15px',
        backgroundColor: '#fef2f2',
        borderRadius: '4px',
        border: '2px solid #fca5a5'
      }}>
        <strong style={{ color: '#991b1b', fontSize: '16px' }}>🔥 Top 3 Rising Stars:</strong>
        <div style={{ marginTop: '10px' }}>
          {data.slice(0, 3).map((artist, index) => (
            <div key={index} style={{ 
              marginBottom: '10px',
              padding: '10px',
              backgroundColor: 'white',
              borderRadius: '4px',
              border: '1px solid #fecaca'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ 
                    display: 'inline-block',
                    width: '24px',
                    height: '24px',
                    borderRadius: '50%',
                    backgroundColor: index === 0 ? '#dc2626' : index === 1 ? '#ea580c' : '#f59e0b',
                    color: 'white',
                    textAlign: 'center',
                    lineHeight: '24px',
                    marginRight: '10px',
                    fontSize: '12px',
                    fontWeight: 'bold'
                  }}>
                    {index + 1}
                  </span>
                  <strong style={{ color: '#1f2937' }}>{artist.artist}</strong>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <div style={{ color: '#dc2626', fontWeight: 'bold', fontSize: '16px' }}>
                    +{artist.growth_rate.toFixed(1)}%
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    {artist.previous_streams.toLocaleString()} → {artist.current_streams.toLocaleString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RisingArtistsChart;
