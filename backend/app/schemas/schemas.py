from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# Genre by region
class GenreByRegionResponse(BaseModel):
    region_name: str
    genre: str
    listen_count: int
    last_updated: datetime

# Subscribers by region
class SubscribersByRegionResponse(BaseModel):
    region_name: str
    level: str
    subscriber_count: int
    last_updated: datetime

# Artist popularity by geo
class ArtistPopularityByGeoResponse(BaseModel):
    state: str
    artist: str
    play_count: int
    unique_listeners: int
    last_updated: datetime

# User engagement by content
class UserEngagementByContentResponse(BaseModel):
    artist: str
    genre: str
    avg_session_length_after_play: int
    repeat_plays: int
    unique_listeners: int
    returning_user_pct: int
    last_updated: datetime

# Retention cohort
class RetentionCohortResponse(BaseModel):
    cohort_month: str
    period: int
    state: str
    retained_users: int
    churned_users: int
    upgrades: int
    downgrades: int
    last_updated: datetime

# City growth trends
class CityGrowthTrendsResponse(BaseModel):
    city: str
    state: str
    date: datetime
    new_users: int
    percent_growth_wow: int
    total_streaming_hours: int
    last_updated: datetime

# Platform usage
class PlatformUsageResponse(BaseModel):
    device_type: str
    region_name: str
    page: str
    active_users: int
    play_count: int
    last_updated: datetime

# Dashboard summary (aggregate schema, not a model)
class DashboardSummaryResponse(BaseModel):
    total_active_users: int
    total_play_count: int
    top_growth_city: Optional[str]
    top_growth_percent: Optional[int]