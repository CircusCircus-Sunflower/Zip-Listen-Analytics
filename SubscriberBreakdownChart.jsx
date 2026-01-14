import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import axios from 'axios';

/**JN
 * SubscriberBreakdownChart Component
 * Task #28 - (P3) 4 - Create subscriber breakdown chart component
 * 
 * Displays a grouped bar chart comparing paid vs free subscribers across US regions
 */
const SubscriberBreakdownChart = ({ apiUrl = 'http://localhost:8000' }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState('all');

  // US Regions for filter dropdown
  const regions = ['all', 'Northeast', 'Southeast', 'Midwest', 'West'];

  useEffect(() => {
    fetchSubscriberData();
  }, [selectedRegion]);

  const fetchSubscriberData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const endpoint = selectedRegion === 'all'
        ? `${apiUrl}/api/subscribers/by-region`
        : `${apiUrl}/api/subscribers/by-region?region=${selectedRegion}`;
      
      const response = await axios.get(endpoint);
      setData(response.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching subscriber data:', err);
      setError(err.message || 'Failed to fetch subscriber data');
      setLoading(false);
    }
  };

  // Transform data for Plotly grouped bar chart
  const getPlotData = () => {
    if (!data || data.length === 0) return [];

    // Get unique regions
    const regionsInData = [...new Set(data.map(d => d.region))];

    // Separate paid and free subscriber data
    const paidData = regionsInData.map(region => {
      const entry = data.find(d => d.region === region && d.level === 'paid');
      return entry ? entry.user_count : 0;
    });

    const freeData = regionsInData.map(region => {
      const entry = data.find(d => d.region === region && d.level === 'free');
      return entry ? entry.user_count : 0;
    });

    return [
      {
        x: regionsInData,
        y: paidData,
        name: 'Paid Subscribers',
        type: 'bar',
        marker: {
          color: '#28a745', // Green for paid
          line: {
            color: '#1e7e34',
            width: 1
          }
        },
        hovertemplate: '<b>%{x}</b><br>' +
                       'Paid: %{y:,} users<br>' +
                       '<extra></extra>',
      },
      {
        x: regionsInData,
        y: freeData,
        name: 'Free Subscribers',
        type: 'bar',
        marker: {
          color: '#6c757d', // Gray for free
          line: {
            color: '#495057',
            width: 1
          }
        },
        hovertemplate: '<b>%{x}</b><br>' +
                       'Free: %{y:,} users<br>' +
                       '<extra></extra>',
      }
    ];
  };

  // Calculate conversion rate (paid / total)
  const getConversionRate = () => {
    if (!data || data.length === 0) return 0;
    
    const totalPaid = data
      .filter(d => d.level === 'paid')
      .reduce((sum, d) => sum + d.user_count, 0);
    
    const totalFree = data
      .filter(d => d.level === 'free')
      .reduce((sum, d) => sum + d.user_count, 0);
    
    const total = totalPaid + totalFree;
    return total > 0 ? ((totalPaid / total) * 100).toFixed(1) : 0;
  };

  const layout = {
    title: {
      text: 'Paid vs Free Subscribers by Region',
      font: { size: 20, family: 'Arial, sans-serif' }
    },
    barmode: 'group',
    xaxis: {
      title: 'Region',
      tickangle: -45,
    },
    yaxis: {
      title: 'Number of Subscribers',
      tickformat: ',',
    },
    hovermode: 'closest',
    showlegend: true,
    legend: {
      orientation: 'h',
      x: 0.5,
      y: 1.15,
      xanchor: 'center',
      yanchor: 'top',
    },
    margin: {
      l: 80,
      r: 50,
      t: 100,
      b: 100,
    },
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#f8f9fa',
    bargap: 0.15,
    bargroupgap: 0.1,
  };

  const config = {
    responsive: true,
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
  };

  if (loading) {
    return (
      <div className="subscriber-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <div className="spinner">Loading subscriber data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="subscriber-chart-container" style={{ padding: '20px' }}>
        <div className="error-message" style={{ 
          color: '#dc3545', 
          backgroundColor: '#f8d7da', 
          padding: '12px', 
          borderRadius: '4px',
          border: '1px solid #f5c6cb'
        }}>
          <strong>Error:</strong> {error}
          <button 
            onClick={fetchSubscriberData}
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
      <div className="subscriber-chart-container" style={{ padding: '20px', textAlign: 'center' }}>
        <p style={{ color: '#6c757d' }}>No subscriber data available</p>
      </div>
    );
  }

  const totalPaid = data
    .filter(d => d.level === 'paid')
    .reduce((sum, d) => sum + d.user_count, 0);
  
  const totalFree = data
    .filter(d => d.level === 'free')
    .reduce((sum, d) => sum + d.user_count, 0);

  return (
    <div className="subscriber-chart-container" style={{ padding: '20px' }}>
      {/* Region Filter */}
      <div className="chart-controls" style={{ marginBottom: '20px' }}>
        <label htmlFor="subscriber-region-filter" style={{ marginRight: '10px', fontWeight: 'bold' }}>
          Filter by Region:
        </label>
        <select
          id="subscriber-region-filter"
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

      {/* Data Summary with Key Metrics */}
      <div className="chart-summary" style={{ 
        marginTop: '20px', 
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '15px'
      }}>
        <div style={{
          padding: '15px',
          backgroundColor: '#d4edda',
          borderRadius: '4px',
          border: '1px solid #c3e6cb'
        }}>
          <div style={{ fontSize: '12px', color: '#155724', marginBottom: '5px' }}>
            PAID SUBSCRIBERS
          </div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#155724' }}>
            {totalPaid.toLocaleString()}
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#e7e8ea',
          borderRadius: '4px',
          border: '1px solid #d6d8db'
        }}>
          <div style={{ fontSize: '12px', color: '#383d41', marginBottom: '5px' }}>
            FREE SUBSCRIBERS
          </div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#383d41' }}>
            {totalFree.toLocaleString()}
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#d1ecf1',
          borderRadius: '4px',
          border: '1px solid #bee5eb'
        }}>
          <div style={{ fontSize: '12px', color: '#0c5460', marginBottom: '5px' }}>
            TOTAL SUBSCRIBERS
          </div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#0c5460' }}>
            {(totalPaid + totalFree).toLocaleString()}
          </div>
        </div>

        <div style={{
          padding: '15px',
          backgroundColor: '#fff3cd',
          borderRadius: '4px',
          border: '1px solid #ffeaa7'
        }}>
          <div style={{ fontSize: '12px', color: '#856404', marginBottom: '5px' }}>
            CONVERSION RATE
          </div>
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#856404' }}>
            {getConversionRate()}%
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubscriberBreakdownChart;
