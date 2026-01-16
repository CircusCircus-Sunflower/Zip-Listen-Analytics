from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ListenEvent(Base):
    __tablename__ = "listen_events"

    id = Column(Integer, primary_key=True, index=True)
    artist = Column(String, index=True)
    song = Column(String)
    duration = Column(Float)
    userId = Column(String, index=True)
    state = Column(String, index=True)
    level = Column(String, index=True)
    genre = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AuthEvent(Base):
    __tablename__ = "auth_events"

    id = Column(Integer, primary_key=True, index=True)
    success = Column(Boolean)
    userId = Column(String, index=True)
    state = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class StatusChangeEvent(Base):
    __tablename__ = "status_change_events"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
    userId = Column(String, index=True)
    state = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SummaryGenreByRegion(Base):
    __tablename__ = "summary_genre_by_region"
    
    region_name = Column(String, primary_key=True)
    genre = Column(String, primary_key=True)
    listen_count = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SummarySubscribersByRegion(Base):
    __tablename__ = "summary_subscribers_by_region"

    region_name = Column(String, primary_key=True)
    level = Column(String, primary_key=True)  # e.g., "paid", "free"
    subscriber_count = Column(Integer)
    last_updated = Column(DateTime)

class SummaryArtistPopularityByGeo(Base):
    __tablename__ = "summary_artist_popularity_by_geo"
    
    state = Column(String, primary_key=True)
    artist = Column(String, primary_key=True)
    play_count = Column(Integer)
    unique_listeners = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SummaryUserEngagementByContent(Base):
    __tablename__ = "summary_user_engagement_by_content"
    
    artist = Column(String, primary_key=True)
    genre = Column(String, primary_key=True)
    avg_session_length_after_play = Column(Integer)  # seconds
    repeat_plays = Column(Integer)
    unique_listeners = Column(Integer)
    returning_user_pct = Column(Integer)  # percentage
    last_updated = Column(DateTime, default=datetime.utcnow)

class SummaryRetentionCohort(Base):
    __tablename__ = "summary_retention_cohort"
    
    cohort_month = Column(String, primary_key=True)  # e.g., "2024-01"
    period = Column(Integer, primary_key=True)  # months since cohort start
    state = Column(String, primary_key=True)
    retained_users = Column(Integer)
    churned_users = Column(Integer)
    upgrades = Column(Integer)
    downgrades = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SummaryCityGrowthTrends(Base):
    __tablename__ = "summary_city_growth_trends"
    
    city = Column(String, primary_key=True)
    state = Column(String, primary_key=True)
    date = Column(DateTime, primary_key=True)
    new_users = Column(Integer)
    percent_growth_wow = Column(Integer)  # week-over-week percentage
    total_streaming_hours = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

class SummaryPlatformUsage(Base):
    __tablename__ = "summary_platform_usage"

    platform = Column(String, primary_key=True)      # web, mobile, desktop
    region_name = Column(String, primary_key=True)   # US regions
    active_users = Column(Integer)
    play_count = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

