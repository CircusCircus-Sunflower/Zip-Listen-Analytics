# Testing Checklist: Tasks #27 & #28

## Pre-Testing Setup ✅

- [ ] Backend is running (`docker-compose ps` shows all services up)
- [ ] Database is seeded with data (`docker-compose exec db psql -U zipuser -d ziplistendb -c "SELECT COUNT(*) FROM listen_events;"` returns > 0)
- [ ] Frontend dependencies installed (`npm install` completed successfully)
- [ ] Environment variables set (`REACT_APP_API_URL=http://localhost:8000` in `frontend/.env`)
- [ ] Frontend is running (accessible at http://localhost:3000)

---

## Task #27: GenreByRegionChart Component 🎸

### Basic Functionality
- [ ] Chart renders without errors
- [ ] Data loads from API endpoint `/api/genres/by-region`
- [ ] Stacked bar chart displays correctly
- [ ] All regions visible on x-axis (Northeast, Southeast, Midwest, West)
- [ ] Multiple genres visible in stacked bars

### Interactive Features
- [ ] Region filter dropdown exists
- [ ] "All Regions" option shows all data
- [ ] Selecting "Northeast" filters to only Northeast data
- [ ] Selecting "Southeast" filters to only Southeast data
- [ ] Selecting "Midwest" filters to only Midwest data
- [ ] Selecting "West" filters to only West data
- [ ] Filter changes trigger API re-fetch

### Visual Elements
- [ ] Chart title displays: "Genre Distribution by US Region"
- [ ] X-axis label: "Region"
- [ ] Y-axis label: "Number of Streams"
- [ ] Legend shows all genres with different colors
- [ ] Hover tooltips appear on bars
- [ ] Tooltips show: Region, Genre, Stream count

### Data Display
- [ ] Summary section shows "Total Streams" with correct number
- [ ] Summary shows "Genres" count
- [ ] Summary shows "Regions" count
- [ ] Numbers formatted with commas (e.g., "1,234,567")

### Error Handling
- [ ] Stop backend: `docker-compose stop backend`
- [ ] Chart shows error message
- [ ] "Retry" button appears
- [ ] Clicking "Retry" attempts to re-fetch data
- [ ] Restart backend: `docker-compose start backend`
- [ ] Retry successfully loads data

### Edge Cases
- [ ] Empty data returns appropriate message
- [ ] Loading state shows "Loading genre data..." spinner
- [ ] Chart is responsive (resize browser window)
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari (if available)

---

## Task #28: SubscriberBreakdownChart Component 👥

### Basic Functionality
- [ ] Chart renders without errors
- [ ] Data loads from API endpoint `/api/subscribers/by-region`
- [ ] Grouped bar chart displays correctly
- [ ] Paid subscribers (green bars) visible
- [ ] Free subscribers (gray bars) visible
- [ ] Bars are grouped by region

### Interactive Features
- [ ] Region filter dropdown exists
- [ ] "All Regions" shows all regions
- [ ] Selecting specific region filters correctly
- [ ] Each region filter triggers API re-fetch
- [ ] Filter updates chart data instantly

### Visual Elements
- [ ] Chart title: "Paid vs Free Subscribers by Region"
- [ ] X-axis label: "Region"
- [ ] Y-axis label: "Number of Subscribers"
- [ ] Legend shows "Paid Subscribers" (green) and "Free Subscribers" (gray)
- [ ] Hover tooltips appear
- [ ] Tooltips show: Region, Type (Paid/Free), User count

### Metrics Cards
- [ ] "PAID SUBSCRIBERS" card displays (green background)
- [ ] Paid count is accurate
- [ ] "FREE SUBSCRIBERS" card displays (gray background)
- [ ] Free count is accurate
- [ ] "TOTAL SUBSCRIBERS" card displays (blue background)
- [ ] Total = Paid + Free (math checks out)
- [ ] "CONVERSION RATE" card displays (yellow background)
- [ ] Conversion rate = (Paid / Total) * 100
- [ ] Percentage formatted with 1 decimal place

### Metrics Grid Layout
- [ ] Four metrics cards arranged in grid
- [ ] Cards are responsive (wrap on smaller screens)
- [ ] Each card has clear label and large number
- [ ] Color coding matches chart colors

### Error Handling
- [ ] Stop backend: `docker-compose stop backend`
- [ ] Chart shows error message
- [ ] "Retry" button works
- [ ] Error styling is clear (red background)
- [ ] Restart backend and verify recovery

### Edge Cases
- [ ] Empty data shows appropriate message
- [ ] Loading state displays properly
- [ ] Chart is responsive
- [ ] Works across different browsers

---

## Dashboard Integration 🖥️

### Header
- [ ] Header displays "🎵 Zip Listen Analytics"
- [ ] Subtitle shows "Executive Dashboard - Music Streaming Insights"
- [ ] "🔄 Refresh Data" button exists
- [ ] Refresh button reloads the page

### Navigation Tabs
- [ ] Four tabs visible: Overview, Genres, Subscribers, Artists
- [ ] "Overview" tab active by default
- [ ] Clicking each tab switches view
- [ ] Active tab has visual indicator (border/highlight)
- [ ] Tab hover effects work

### Overview Tab
- [ ] Shows grid with all components
- [ ] GenreByRegionChart visible
- [ ] SubscriberBreakdownChart visible
- [ ] Two placeholder cards for tasks #29 and #30
- [ ] Placeholders show "Coming soon..." message
- [ ] Grid is responsive (wraps on smaller screens)

### Genres Tab
- [ ] Shows only GenreByRegionChart
- [ ] Chart is full-width
- [ ] No other charts visible

### Subscribers Tab
- [ ] Shows only SubscriberBreakdownChart
- [ ] Chart is full-width
- [ ] Metrics cards still visible

### Artists Tab
- [ ] Shows two placeholders
- [ ] "🎤 Top Artists" placeholder visible
- [ ] "📈 Rising Artists" placeholder visible
- [ ] Placeholders clearly marked as tasks #29 and #30

### Footer
- [ ] Footer displays project info
- [ ] API status indicator shows "● Connected" in green

### Responsive Design
- [ ] Test at 1920px width (desktop)
- [ ] Test at 1024px width (tablet)
- [ ] Test at 768px width (mobile)
- [ ] Charts resize appropriately
- [ ] Navigation remains functional
- [ ] Cards stack vertically on mobile

---

## API Integration ⚡

### Backend API Endpoints
Test these manually before running frontend:

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Genres endpoint - all regions
curl http://localhost:8000/api/genres/by-region
# Expected: JSON array with region, genre, stream_count

# Genres endpoint - specific region
curl "http://localhost:8000/api/genres/by-region?region=Northeast"
# Expected: Filtered JSON array

# Subscribers endpoint - all regions
curl http://localhost:8000/api/subscribers/by-region
# Expected: JSON array with region, level, user_count

# Subscribers endpoint - specific region
curl "http://localhost:8000/api/subscribers/by-region?region=West"
# Expected: Filtered JSON array
```

### API Response Validation
- [ ] All endpoints return valid JSON
- [ ] No CORS errors in browser console
- [ ] Response times < 1 second
- [ ] Data structure matches expected format
- [ ] No 500 errors in backend logs

---

## Browser Console Checks 🔍

Open browser DevTools (F12) and check:

### Console Tab
- [ ] No JavaScript errors
- [ ] No React warnings
- [ ] API calls logged (if using console.log)
- [ ] No CORS errors

### Network Tab
- [ ] API requests show status 200 OK
- [ ] Response payload matches expected format
- [ ] Request timing is reasonable
- [ ] No failed requests (except during error testing)

### React DevTools (if installed)
- [ ] Components render in correct hierarchy
- [ ] Props are passed correctly
- [ ] State updates properly on filter changes

---

## Performance Checks ⚡

- [ ] Initial page load < 3 seconds
- [ ] Chart data loads < 2 seconds
- [ ] Filter changes reflect instantly
- [ ] No lag when switching tabs
- [ ] Smooth animations and transitions
- [ ] No memory leaks (check DevTools Performance tab)

---

## Accessibility Checks ♿

- [ ] All interactive elements keyboard accessible
- [ ] Tab key navigates through filters and buttons
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG standards
- [ ] Charts have descriptive labels
- [ ] Error messages are clear and actionable

---

## Code Quality Checks ✨

### JavaScript/React
- [ ] No console.log statements (remove before commit)
- [ ] Proper PropTypes or TypeScript (if using)
- [ ] Clean code formatting (consistent indentation)
- [ ] Comments explain complex logic
- [ ] Component names are descriptive

### CSS
- [ ] No unused styles
- [ ] Consistent class naming convention
- [ ] Responsive breakpoints work
- [ ] No inline styles (use classes)
- [ ] Print styles tested (Cmd/Ctrl + P)

---

## Git & Documentation ✅

- [ ] All files added to Git
- [ ] Commit message follows convention
- [ ] Branch named appropriately (`feature/tasks-27-28`)
- [ ] README updated (if needed)
- [ ] IMPLEMENTATION_GUIDE.md reviewed
- [ ] No sensitive data in commits (passwords, keys, etc.)

---

## Final Verification 🎯

Before marking tasks as complete:

- [ ] Both components work independently
- [ ] Both components work in Dashboard
- [ ] All filters functional
- [ ] Error handling tested
- [ ] Responsive design verified
- [ ] Code is clean and documented
- [ ] Git commit prepared
- [ ] Kanban board ready to update (#27 → Done, #28 → Done)

---

## Known Issues / Notes 📝

Document any issues found during testing:

```
Issue: [Describe issue]
Severity: [Low/Medium/High]
Status: [Open/Fixed]
Notes: [Additional context]
```

---

## Test Results Summary 📊

After completing all tests, fill in:

- **Date Tested**: _____________
- **Tester Name**: _____________
- **Total Tests**: _____________
- **Tests Passed**: _____________
- **Tests Failed**: _____________
- **Overall Status**: [ ] PASS [ ] FAIL [ ] NEEDS REVIEW

### Critical Failures (if any):
_____________________________________________
_____________________________________________

### Recommendations:
_____________________________________________
_____________________________________________

---

## Sign-off ✍️

Tasks #27 and #28 are ready for:
- [ ] Code review
- [ ] Merge to dev branch
- [ ] Marking as "Done" on Kanban board
- [ ] Demo to team/stakeholders

**Tested by**: _________________  
**Date**: _________________  
**Approved by**: _________________  
**Date**: _________________
