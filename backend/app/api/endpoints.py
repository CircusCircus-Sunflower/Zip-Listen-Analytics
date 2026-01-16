from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from sqlalchemy import and_
import pandas as pd

# Utility/database imports
from ..db.database import get_db

# Import ALL relevant models (event + summary tables)
from ..models.models import (
    ListenEvent,
    StatusChangeEvent,
    # Add all summary models below!
    SummaryGenreByRegion,
    SummaryRetentionCohort,
    SummarySubscribersByRegion,
    SummaryArtistPopularityByGeo,
    SummaryUserEngagementByContent,
    SummaryCityGrowthTrends,
    SummaryPlatformUsage
)

# Import ALL response schemas
from ..schemas.schemas import (
    GenreByRegionResponse,
    SubscribersByRegionResponse,
    ArtistPopularityByGeoResponse,
    UserEngagementByContentResponse,
    RetentionCohortResponse,                # <-- If you keep retention endpoints
    CityGrowthTrendsResponse,
    PlatformUsageResponse,
    DashboardSummaryResponse
)
from ..utils.regions import STATE_TO_REGION

router = APIRouter()


@router.get("/genres/by-region", response_model=List[GenreByRegionResponse])
def get_genres_by_region(
    region: Optional[str] = Query(None, description="Filter by specific region"),
    db: Session = Depends(get_db)
):
    """
    Get genre distribution by US region (Northeast, Southeast, Midwest, West)
    """
    from ..models.models import SummaryGenreByRegion
    
    # Query summary table
    query = db.query(SummaryGenreByRegion)
    
    # Filter by region if specified
    if region:
        query = query.filter(SummaryGenreByRegion.region_name == region)
    
    # Return results directly
    return [
        GenreByRegionResponse(
            region=row.region_name,
            genre=row.genre,
            listen_count=row.listen_count
        ) for row in query.all()
    ]


@router.get("/subscribers/by-region", response_model=List[SubscribersByRegionResponse])
def get_subscribers_by_region(
    region_name: Optional[str] = Query(None),
    level: Optional[str] = Query(None),  # allow optional filter by paid/free
    db: Session = Depends(get_db)
):
    query = db.query(SummarySubscribersByRegion)
    if region_name:
        query = query.filter(SummarySubscribersByRegion.region_name == region_name)
    if level:
        query = query.filter(SummarySubscribersByRegion.level == level)
    return [
        SubscribersByRegionResponse(
            region_name=row.region_name,
            level=row.level,
            subscriber_count=row.subscriber_count,
            last_updated=row.last_updated
        ) for row in query.all()
    ]


@router.get("/artists/top", response_model=list[ArtistPopularityByGeoResponse])
def get_top_artist_per_state(
    db: Session = Depends(get_db),
):
    # Find the MAX play_count per state (subquery)
    subq = (
        db.query(
            SummaryArtistPopularityByGeo.state,
            func.max(SummaryArtistPopularityByGeo.play_count).label("max_play_count")
        )
        .group_by(SummaryArtistPopularityByGeo.state)
        .subquery()
    )

    # Join to main table to get the top artist per state
    results = (
        db.query(SummaryArtistPopularityByGeo)
        .join(
            subq,
            and_(
                SummaryArtistPopularityByGeo.state == subq.c.state,
                SummaryArtistPopularityByGeo.play_count == subq.c.max_play_count
            )
        )
        .all()
    )

    return [
        ArtistPopularityByGeoResponse(
            state=row.state,
            artist=row.artist,
            play_count=row.play_count,
            unique_listeners=row.unique_listeners,
            last_updated=row.last_updated
        )
        for row in results
    ]


@router.get("/artists/rising", response_model=List[UserEngagementByContentResponse])
def get_rising_artists(
    db: Session = Depends(get_db)
):
    query = db.query(SummaryUserEngagementByContent)
    # Sort by repeat_plays descending as "rising" proxy
    results = query.order_by(SummaryUserEngagementByContent.repeat_plays.desc()).all()
    return [
        UserEngagementByContentResponse(
            artist=row.artist,
            genre=row.genre,
            avg_session_length_after_play=row.avg_session_length_after_play,
            repeat_plays=row.repeat_plays,
            unique_listeners=row.unique_listeners,
            returning_user_pct=row.returning_user_pct,
            last_updated=row.last_updated
        )
        for row in results
    ]

@router.get("/cities/growth", response_model=List[CityGrowthTrendsResponse])
def get_city_growth(
    state: Optional[str] = Query(None, description="Filter by state"),
    db: Session = Depends(get_db)
):
    query = db.query(SummaryCityGrowthTrends)
    if state:
        query = query.filter(SummaryCityGrowthTrends.state == state)
    return [
        CityGrowthTrendsResponse(
            city=row.city,
            state=row.state,
            date=row.date,
            new_users=row.new_users,
            percent_growth_wow=row.percent_growth_wow,
            total_streaming_hours=row.total_streaming_hours
        ) for row in query.all()
    ]

@router.get("/platforms/usage", response_model=List[PlatformUsageResponse])
def get_platform_usage(
    platform: Optional[str] = Query(None, description="Filter by platform"),
    db: Session = Depends(get_db)
):
    query = db.query(SummaryPlatformUsage)
    if platform:
        query = query.filter(SummaryPlatformUsage.platform == platform)
    return [
        PlatformUsageResponse(
            platform=row.platform,
            region_name=row.region_name,
            active_users=row.active_users,
            play_count=row.play_count
        ) for row in query.all()
    ]

@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    # Total users from platform usage
    total_users = db.query(func.sum(SummaryPlatformUsage.active_users)).scalar() or 0
    total_plays = db.query(func.sum(SummaryPlatformUsage.play_count)).scalar() or 0

    # Latest city with max growth
    city_growth = db.query(SummaryCityGrowthTrends).order_by(
        SummaryCityGrowthTrends.percent_growth_wow.desc()
    ).first()

    return DashboardSummaryResponse(
        total_active_users=total_users,
        total_play_count=total_plays,
        top_growth_city=city_growth.city if city_growth else None,
        top_growth_percent=city_growth.percent_growth_wow if city_growth else None,
    )

@router.get("/retention", response_model=List[RetentionCohortResponse])
def get_retention_data(
    cohort_month: Optional[str] = Query(None, description="Cohort month (YYYY-MM)"),
    state: Optional[str] = Query(None, description="US state abbreviation (e.g., 'NY', 'TX')"),
    db: Session = Depends(get_db)
):
    query = db.query(SummaryRetentionCohort)
    if cohort_month:
        query = query.filter(SummaryRetentionCohort.cohort_month == cohort_month)
    if state:
        query = query.filter(SummaryRetentionCohort.state == state)
    return [
        RetentionCohortResponse(
            cohort_month=row.cohort_month,
            period=row.period,
            state=row.state,
            retained_users=row.retained_users,
            churned_users=row.churned_users,
            upgrades=row.upgrades,
            downgrades=row.downgrades,
            last_updated=row.last_updated
        ) for row in query.all()
    ]