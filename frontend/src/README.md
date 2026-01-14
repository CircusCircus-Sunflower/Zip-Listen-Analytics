name: services/README.md
---
# services
Contains API service wrapper for backend HTTP calls.

Files:
- api.js — Axios client and exported functions:
  - getGenresByRegion(region)
  - getSubscribersByRegion(region)
  - getTopArtists(limit)
  - getRisingArtists(limit)

Notes:
- Base URL reads from REACT_APP_API_URL.
- Keep functions thin and return axios responses (res.data).

JN