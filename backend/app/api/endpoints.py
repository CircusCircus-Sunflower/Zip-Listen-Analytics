from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import pandas as pd

from ..db.database import get_db
from ..models.models import ListenEvent, StatusChangeEvent
from ..schemas.schemas import (
    GenreByRegionResponse,
    SubscriberByRegionResponse,
    TopArtistResponse,
    RisingArtistResponse
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
            stream_count=row.listen_count
        ) for row in query.all()
    ]


@router.get("/subscribers/by-region", response_model=List[SubscriberByRegionResponse])
def get_subscribers_by_region(
    region: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(SummaryRetentionCohort)
    if region:
        query = query.filter(SummaryRetentionCohort.region_name == region)  # If your table has region_name!
    # Adjust fields according to your table!
    return [
        SubscriberByRegionResponse(
            cohort_month=row.cohort_month,
            retained_users=row.retained_users,
            churned_users=row.churned_users,
            upgrades=row.upgrades,
            downgrades=row.downgrades
        ) for row in query.all()
    ]


@router.get("/artists/top", response_model=List[TopArtistsResponse])
def get_top_artists(
    region: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(SummaryArtistPopularityByGeo)
    if region:
        query = query.filter(SummaryArtistPopularityByGeo.region_name == region)
    query = query.order_by(SummaryArtistPopularityByGeo.play_count.desc())
    return [
        TopArtistsResponse(
            artist=row.artist,
            region=row.region_name,
            play_count=row.play_count,
            unique_listeners=row.unique_listeners
        ) for row in query.all()
    ]


@router.get("/artists/rising", response_model=List[RisingArtistResponse])
def get_rising_artists(
    db: Session = Depends(get_db)
):
    query = db.query(SummaryUserEngagementByContent)
    # Add additional sorting or filtering as needed for "rising" logic
    results = query.order_by(SummaryUserEngagementByContent.repeat_plays.desc()).all()
    return [
        RisingArtistResponse(
            artist=row.artist,
            song=row.song,
            repeat_plays=row.repeat_plays,
            returning_user_pct=row.returning_user_pct
        ) for row in results
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