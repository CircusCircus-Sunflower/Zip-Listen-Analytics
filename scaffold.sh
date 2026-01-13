#!/usr/bin/env bash
set -euo pipefail

# Make dirs
mkdir -p frontend/src/services frontend/src/components frontend/src/pages

backup_if_exists() {
  target="$1"
  if [ -f "$target" ]; then
    ts=$(date +%s)
    mv "$target" "${target}.bak.$ts"
    echo "Backed up $target -> ${target}.bak.$ts"
  fi
}

# Example: write services/api.js
target="frontend/src/services/api.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'\;

const client = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

export async function getGenresByRegion(region = null) {
  return client.get('/api/genres/by-region', { params: region ? { region } : {} });
}

export async function getSubscribersByRegion(region = null) {
  return client.get('/api/subscribers/by-region', { params: region ? { region } : {} });
}

export async function getTopArtists(limit = 10) {
  return client.get('/api/artists/top', { params: { limit } });
}

export async function getRisingArtists(limit = 10) {
  return client.get('/api/artists/rising', { params: { limit } });
}

export default {
  getGenresByRegion,
  getSubscribersByRegion,
  getTopArtists,
  getRisingArtists
};
EOF

# PlotlyChart
target="frontend/src/components/PlotlyChart.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import React from 'react';
import Plot from 'react-plotly.js';

export default function PlotlyChart({ data, layout, config, onPointClick, style }) {
  const mergedLayout = { margin: { t: 40, l: 50, r: 20, b: 50 }, ...layout };

  return (
    <div style={style}>
      <Plot
        data={data}
        layout={mergedLayout}
        config={{ responsive: true, displayModeBar: true, ...config }}
        onClick={(evt) => {
          if (onPointClick && evt && evt.points && evt.points.length) {
            onPointClick(evt.points[0]);
          }
        }}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
EOF

# Header
target="frontend/src/components/Header.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import React from 'react';

export default function Header({ title = 'Zip Listen Analytics', apiUrl, onRefresh }) {
  return (
    <header className="App-header" style={{ padding: '1.5rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ margin: 0 }}>{title}</h1>
          <p style={{ margin: '4px 0 0 0', opacity: 0.9 }}>Executive Dashboard</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ marginBottom: 8, opacity: 0.85 }}>API: <strong>{apiUrl}</strong></div>
          <button className="refresh-btn" onClick={onRefresh}>Refresh</button>
        </div>
      </div>
    </header>
  );
}
EOF

# FiltersPanel
target="frontend/src/components/FiltersPanel.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import React, { useState } from 'react';

export default function FiltersPanel({ onApply }) {
  const [region, setRegion] = useState('All');
  const [range, setRange] = useState('30d');
  const [level, setLevel] = useState('All');

  function apply() {
    onApply({
      region: region === 'All' ? null : region,
      range,
      level: level === 'All' ? null : level
    });
  }

  return (
    <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap', margin: '1rem 0' }}>
      <label>
        Region:
        <select value={region} onChange={e => setRegion(e.target.value)} style={{ marginLeft: 6 }}>
          <option>All</option>
          <option>Northeast</option>
          <option>Southeast</option>
          <option>Midwest</option>
          <option>West</option>
        </select>
      </label>

      <label>
        Time:
        <select value={range} onChange={e => setRange(e.target.value)} style={{ marginLeft: 6 }}>
          <option value="7d">7d</option>
          <option value="30d">30d</option>
          <option value="90d">90d</option>
        </select>
      </label>

      <label>
        Level:
        <select value={level} onChange={e => setLevel(e.target.value)} style={{ marginLeft: 6 }}>
          <option>All</option>
          <option>paid</option>
          <option>free</option>
        </select>
      </label>

      <button className="refresh-btn" onClick={apply}>Apply</button>
    </div>
  );
}
EOF

# ChartCard
target="frontend/src/components/ChartCard.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import React from 'react';

export default function ChartCard({ title, subtitle, children }) {
  return (
    <div className="chart-container" role="region" aria-label={title} style={{ minHeight: 300 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <div>
          <h3 style={{ margin: 0, color: '#111' }}>{title}</h3>
          {subtitle && <small style={{ color: '#444' }}>{subtitle}</small>}
        </div>
      </div>
      <div style={{ width: '100%', height: '100%' }}>
        {children}
      </div>
    </div>
  );
}
EOF

# Dashboard (abbreviated write)
target="frontend/src/pages/Dashboard.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import React, { useState, useEffect, useMemo } from 'react';
import Header from '../components/Header';
import FiltersPanel from '../components/FiltersPanel';
import ChartCard from '../components/ChartCard';
import PlotlyChart from '../components/PlotlyChart';
import api from '../services/api';
import '../App.css';

export default function Dashboard() {
  const [genresData, setGenresData] = useState([]);
  const [subscribersData, setSubscribersData] = useState([]);
  const [topArtistsData, setTopArtistsData] = useState([]);
  const [risingArtistsData, setRisingArtistsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000'\;
  const [lastUpdated, setLastUpdated] = useState(null);

  async function fetchAll() {
    setLoading(true);
    try {
      const [genresRes, subsRes, topRes, risingRes] = await Promise.all([
        api.getGenresByRegion(filters.region),
        api.getSubscribersByRegion(filters.region),
        api.getTopArtists(10),
        api.getRisingArtists(10)
      ]);
      setGenresData(genresRes.data || []);
      setSubscribersData(subsRes.data || []);
      setTopArtistsData(topRes.data || []);
      setRisingArtistsData(risingRes.data || []);
      setLastUpdated(new Date().toISOString());
    } catch (err) {
      console.error('API error', err);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { fetchAll(); }, [filters]);

  const genresChart = useMemo(() => {
    if (!genresData || genresData.length === 0) return null;
    const regions = [...new Set(genresData.map(d => d.region))];
    const genres = [...new Set(genresData.map(d => d.genre))];
    const traces = genres.map(genre => ({
      x: regions,
      y: regions.map(region => {
        const item = genresData.find(d => d.region === region && d.genre === genre);
        return item ? item.stream_count : 0;
      }),
      name: genre,
      type: 'bar'
    }));
    return { data: traces, layout: { title: 'Genre Distribution by Region', barmode: 'stack', xaxis: { title: 'Region' }, yaxis: { title: 'Streams' } } };
  }, [genresData]);

  const subsChart = useMemo(() => {
    if (!subscribersData || subscribersData.length === 0) return null;
    const regions = [...new Set(subscribersData.map(d => d.region))];
    const paid = regions.map(region => (subscribersData.find(d => d.region === region && d.level === 'paid')?.user_count || 0));
    const free = regions.map(region => (subscribersData.find(d => d.region === region && d.level === 'free')?.user_count || 0));
    return { data: [
      { x: regions, y: paid, name: 'Paid', type: 'bar', marker: { color: '#4CAF50' } },
      { x: regions, y: free, name: 'Free', type: 'bar', marker: { color: '#2196F3' } }
    ], layout: { title: 'Subscribers by Region', barmode: 'group', xaxis: { title: 'Region' }, yaxis: { title: 'Users' } } };
  }, [subscribersData]);

  return (
    <div className="App">
      <Header apiUrl={apiUrl} onRefresh={fetchAll} />
      <main style={{ padding: '1rem', maxWidth: 1400, margin: '0 auto' }}>
        <FiltersPanel onApply={setFilters} />
        {loading && <div className="loading">Loading data…</div>}
        {!loading &&
          <div className="dashboard" aria-live="polite">
            <ChartCard title="Genre Distribution">
              {genresChart ? <PlotlyChart data={genresChart.data} layout={genresChart.layout} /> : <div>No data</div>}
            </ChartCard>
            <ChartCard title="Subscribers">
              {subsChart ? <PlotlyChart data={subsChart.data} layout={subsChart.layout} /> : <div>No data</div>}
            </ChartCard>
            <ChartCard title="Top Artists" subtitle="Top streamed artists">
              <div style={{ padding: 8 }}>
                <ol>
                  {topArtistsData.map((a, i) => <li key={a.artist || i}><strong>{a.artist}</strong> — {a.stream_count} streams</li>)}
                </ol>
              </div>
            </ChartCard>
            <ChartCard title="Rising Artists" subtitle="Fastest growth">
              <div style={{ padding: 8 }}>
                <ol>
                  {risingArtistsData.map((a, i) => <li key={a.artist || i}><strong>{a.artist}</strong> — {a.growth_rate}%</li>)}
                </ol>
              </div>
            </ChartCard>
          </div>
        }
      </main>
      <footer className="App-footer">
        <p>Data from API — last updated: {lastUpdated || '-'}</p>
      </footer>
    </div>
  );
}
EOF

# App.js replacement
target="frontend/src/App.js"
backup_if_exists "$target"
cat > "$target" <<'EOF'
import React from 'react';
import Dashboard from './pages/Dashboard';
import './App.css';

function App() {
  return <Dashboard />;
}

export default App;
EOF

git add frontend/src/services frontend/src/components frontend/src/pages frontend/src/App.js
git commit -m "feat(frontend): scaffold API service and dashboard UI components (scripted)"
git push -u origin "$(git rev-parse --abbrev-ref HEAD)"
echo "Scaffold complete and pushed."
