# Implementation Guide: Tasks #27 & #28

## Overview
This guide covers the implementation of:
- **Task #27**: Genre by Region Chart Component
- **Task #28**: Subscriber Breakdown Chart Component

## 📦 Files Created

### 1. GenreByRegionChart.jsx
**Location**: `frontend/src/components/GenreByRegionChart.jsx`

**Features**:
- Stacked bar chart showing genre distribution across US regions
- Region filter dropdown (All, Northeast, Southeast, Midwest, West)
- Real-time data fetching from backend API
- Error handling and retry functionality
- Summary statistics (total streams, genre count, region count)
- Responsive design with hover tooltips

**API Endpoint**: `GET /api/genres/by-region?region={region}`

### 2. SubscriberBreakdownChart.jsx
**Location**: `frontend/src/components/SubscriberBreakdownChart.jsx`

**Features**:
- Grouped bar chart comparing paid vs free subscribers
- Region filter dropdown
- Key metrics display:
  - Total paid subscribers
  - Total free subscribers
  - Total subscribers
  - Conversion rate (paid/total %)
- Color-coded metrics cards
- Interactive Plotly chart

**API Endpoint**: `GET /api/subscribers/by-region?region={region}`

### 3. Dashboard.jsx
**Location**: `frontend/src/components/Dashboard.jsx`

**Features**:
- Main dashboard with tabbed navigation
- Integrates both chart components
- Overview grid showing all analytics
- Individual tabs for detailed views
- Placeholders for tasks #29 and #30
- Responsive layout

### 4. Dashboard.css
**Location**: `frontend/src/components/Dashboard.css`

**Features**:
- Modern gradient background
- Card-based layout
- Smooth animations and transitions
- Responsive breakpoints
- Print-friendly styles

---

## 🚀 Installation Steps

### 1. Copy Files to Your Frontend Directory

```bash
# From your project root
cd ~/Projects/Zip-Listen-Analytics/frontend/src

# Create components directory if it doesn't exist
mkdir -p components

# Copy the component files (you'll need to download these from the chat)
# Place them in frontend/src/components/
```

### 2. Install Required Dependencies

```bash
cd ~/Projects/Zip-Listen-Analytics/frontend

# Install Plotly for React (if not already installed)
npm install react-plotly.js plotly.js

# Install axios for API calls (if not already installed)
npm install axios

# Install and verify all dependencies
npm install
```

### 3. Update Your App.js

Update `frontend/src/App.js` to include the Dashboard:

```javascript
import React from 'react';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <div className="App">
      <Dashboard />
    </div>
  );
}

export default App;
```

### 4. Set Environment Variables

Create or update `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🧪 Testing Instructions

### 1. Ensure Backend is Running

```bash
# From project root
cd ~/Projects/Zip-Listen-Analytics

# Start all services
docker-compose up -d

# Check services are running
docker-compose ps

# Verify backend API is accessible
curl http://localhost:8000/health
curl http://localhost:8000/api/genres/by-region
curl http://localhost:8000/api/subscribers/by-region
```

### 2. Start Frontend Development Server

```bash
# Option A: If running outside Docker
cd frontend
npm start

# Option B: If using Docker (recommended)
docker-compose up -d frontend
docker-compose logs -f frontend
```

### 3. Access the Application

Open your browser to: **http://localhost:3000**

### 4. Test Chart Functionality

#### Genre Chart Tests:
1. ✅ Chart loads with data
2. ✅ Region filter dropdown works
3. ✅ Selecting "All Regions" shows all data
4. ✅ Selecting specific region filters correctly
5. ✅ Hover tooltips display correctly
6. ✅ Summary statistics are accurate
7. ✅ Error handling works (stop backend and verify error message)
8. ✅ Retry button re-fetches data

#### Subscriber Chart Tests:
1. ✅ Chart loads with paid/free comparison
2. ✅ Region filter works correctly
3. ✅ Metrics cards display correct totals
4. ✅ Conversion rate calculation is accurate
5. ✅ Color coding is clear (green=paid, gray=free)
6. ✅ Hover tooltips work
7. ✅ Error handling and retry work

#### Dashboard Tests:
1. ✅ All tabs switch correctly (Overview, Genres, Subscribers, Artists)
2. ✅ Overview grid shows both charts
3. ✅ Individual tabs show full-width charts
4. ✅ Refresh button reloads data
5. ✅ Responsive layout works on different screen sizes
6. ✅ Placeholders show for tasks #29 and #30

---

## 🔧 Troubleshooting

### Issue: Charts not loading

**Solution 1**: Check if backend API is running
```bash
curl http://localhost:8000/api/genres/by-region
# Should return JSON data
```

**Solution 2**: Check CORS settings in backend
Ensure `app/main.py` has CORS middleware:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: "react-plotly.js" not found

```bash
cd frontend
npm install react-plotly.js plotly.js --save
docker-compose restart frontend
```

### Issue: API URL not working

Check `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
```

Restart frontend after changing .env:
```bash
docker-compose restart frontend
```

### Issue: No data showing in charts

**Check database has data**:
```bash
docker-compose exec db psql -U zipuser -d ziplistendb -c "SELECT COUNT(*) FROM listen_events;"
# Should return > 0
```

If count is 0, re-seed database:
```bash
docker exec -i ziplisten-db psql -U zipuser -d ziplistendb < init_db.sql
```

---

## 📝 Component API Documentation

### GenreByRegionChart Props

```javascript
<GenreByRegionChart 
  apiUrl={string}  // Default: 'http://localhost:8000'
/>
```

### SubscriberBreakdownChart Props

```javascript
<SubscriberBreakdownChart 
  apiUrl={string}  // Default: 'http://localhost:8000'
/>
```

### Dashboard Props

```javascript
<Dashboard />  // No props required
```

---

## 🎨 Customization Guide

### Changing Chart Colors

**GenreByRegionChart** - Colors are auto-assigned by Plotly. To customize:
```javascript
// In getPlotData(), add marker property:
marker: {
  color: '#your-color-here'
}
```

**SubscriberBreakdownChart** - Update colors in getPlotData():
```javascript
marker: {
  color: '#28a745',  // Change paid color here
}
```

### Modifying Layout

Update `Dashboard.css`:
- Grid columns: `.overview-grid { grid-template-columns: ... }`
- Card sizing: `.chart-card { ... }`
- Colors: Update CSS variables

### Adding More Filters

To add date range filters or other controls:
1. Add state in component: `const [dateRange, setDateRange] = useState()`
2. Add UI control in JSX
3. Update API call to include new parameters
4. Modify backend endpoint if needed

---

## 🔄 Git Workflow for These Changes

### Option 1: Create Feature Branch (Recommended)

```bash
# From project root
cd ~/Projects/Zip-Listen-Analytics

# Create and switch to feature branch
git checkout -b feature/tasks-27-28-chart-components

# Add the new files
git add frontend/src/components/GenreByRegionChart.jsx
git add frontend/src/components/SubscriberBreakdownChart.jsx
git add frontend/src/components/Dashboard.jsx
git add frontend/src/components/Dashboard.css
git add frontend/src/App.js
git add frontend/.env
git add frontend/package.json

# Commit
git commit -m "feat: add genre and subscriber chart components (tasks #27, #28)

- Add GenreByRegionChart with region filtering
- Add SubscriberBreakdownChart with metrics cards
- Integrate both charts in Dashboard component
- Add responsive styling and error handling
- Tasks: #27, #28"

# Push to remote
git push origin feature/tasks-27-28-chart-components
```

### Option 2: Commit Directly to Dev (After teammate updates)

```bash
# Wait for teammate to push their changes
# Then pull latest dev
git checkout dev
git pull origin dev --rebase

# Add your files
git add frontend/src/components/*
git commit -m "feat: add chart components for tasks #27 and #28"
git push origin dev
```

---

## 📊 Success Criteria

Tasks #27 and #28 are complete when:

- [x] GenreByRegionChart component created and functional
- [x] SubscriberBreakdownChart component created and functional
- [x] Both charts fetch data from backend API
- [x] Region filtering works correctly
- [x] Error handling is implemented
- [x] Charts are responsive
- [x] Dashboard integrates both components
- [x] Code is documented with comments
- [x] Components follow React best practices
- [x] Files committed to Git with proper messages

---

## 📌 Next Steps (Tasks #29, #30)

After completing #27 and #28, the next components to build are:

### Task #29: Top Artists List Component
- Bar chart showing top 10 artists by stream count
- API endpoint: `GET /api/artists/top?limit=10`

### Task #30: Rising Artists Component
- Bar chart showing rising artists by growth rate
- API endpoint: `GET /api/artists/rising?limit=10`

Both will follow similar patterns to the charts you just created!

---

## 🤝 Team Collaboration Notes

- **Before committing**: Ensure your local dev branch is up to date
- **Code reviews**: Create pull requests for feature branches
- **Testing**: Always test locally before pushing
- **Documentation**: Update README.md with any new setup steps
- **Communication**: Update Kanban board when tasks are completed

---

## 📞 Need Help?

If you encounter issues:
1. Check the Troubleshooting section above
2. Review backend logs: `docker-compose logs backend`
3. Review frontend logs: `docker-compose logs frontend`
4. Check browser console for JavaScript errors
5. Verify API responses in browser Network tab

Good luck with the implementation! 🚀
