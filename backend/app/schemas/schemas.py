from pydantic import BaseModel
from typing import List, Optional


class GenreByRegionResponse(BaseModel):
    region: str
    genre: str
    stream_count: int


class SubscriberByRegionResponse(BaseModel):
    region: str
    level: str
    user_count: int


class TopArtistResponse(BaseModel):
    artist: str
    stream_count: int
    rank: int


class RisingArtistResponse(BaseModel):
    artist: str
    growth_rate: float
    current_streams: int
    previous_streams: int

class CityGrowthTrendsResponse(BaseModel):
    city: str
    state: str
    date: date
    new_users: int
    percent_growth_wow: int
    total_streaming_hours: int

class PlatformUsageResponse(BaseModel):
    platform: str
    region_name: str
    active_users: int
    play_count: int

class DashboardSummaryResponse(BaseModel):
    total_active_users: int
    total_play_count: int
    top_growth_city: Optional[str]
    top_growth_percent: Optional[float]