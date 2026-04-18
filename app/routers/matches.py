"""
Match CRUD endpoints.
Provides full Create, Read, Update, Delete operations for football matches.
"""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.match import Match
from app.models.team import Team
from app.schemas.match import MatchCreate, MatchUpdate, MatchResponse, MatchListResponse
from app.utils.auth import require_auth
from app.models.user import User

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("/", response_model=MatchListResponse, summary="List all matches")
def list_matches(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    season: Optional[str] = Query(None, description="Filter by season"),
    team_id: Optional[int] = Query(None, description="Filter by team (home or away)"),
    date_from: Optional[date] = Query(None, description="Filter matches from this date"),
    date_to: Optional[date] = Query(None, description="Filter matches until this date"),
    matchday: Optional[int] = Query(None, description="Filter by matchday"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of matches with optional filtering.
    
    Supports filtering by season, team, date range, and matchday.
    """
    query = db.query(Match)
    
    if season:
        query = query.filter(Match.season == season)
    if team_id:
        query = query.filter(
            (Match.home_team_id == team_id) | (Match.away_team_id == team_id)
        )
    if date_from:
        query = query.filter(Match.match_date >= date_from)
    if date_to:
        query = query.filter(Match.match_date <= date_to)
    if matchday:
        query = query.filter(Match.matchday == matchday)

    if date_from and date_to and date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_from cannot be later than date_to"
        )
    
    query = query.order_by(Match.match_date.desc(), Match.id.desc())
    
    total = query.count()
    matches = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return MatchListResponse(
        total=total,
        page=page,
        page_size=page_size,
        matches=matches
    )


@router.get("/{match_id}", response_model=MatchResponse, summary="Get match by ID")
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific match by its ID."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    return match


@router.post("/", response_model=MatchResponse, status_code=status.HTTP_201_CREATED, summary="Create a new match")
def create_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Create a new match record. Requires authentication.
    
    Both home_team_id and away_team_id must reference existing teams.
    """
    # Validate teams exist
    home_team = db.query(Team).filter(Team.id == match_data.home_team_id).first()
    if not home_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Home team with id {match_data.home_team_id} not found"
        )
    
    away_team = db.query(Team).filter(Team.id == match_data.away_team_id).first()
    if not away_team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Away team with id {match_data.away_team_id} not found"
        )

    if match_data.home_team_id == match_data.away_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Home team and away team cannot be the same"
        )
    
    match = Match(**match_data.model_dump())
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.put("/{match_id}", response_model=MatchResponse, summary="Update a match")
def update_match(
    match_id: int,
    match_data: MatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Update an existing match. Requires authentication.
    
    Only provided fields will be updated (partial update supported).
    """
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    
    update_data = match_data.model_dump(exclude_unset=True)

    home_team_id = update_data.get("home_team_id", match.home_team_id)
    away_team_id = update_data.get("away_team_id", match.away_team_id)

    if home_team_id == away_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Home team and away team cannot be the same"
        )

    if "home_team_id" in update_data:
        home_team = db.query(Team).filter(Team.id == home_team_id).first()
        if not home_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Home team with id {home_team_id} not found"
            )
    if "away_team_id" in update_data:
        away_team = db.query(Team).filter(Team.id == away_team_id).first()
        if not away_team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Away team with id {away_team_id} not found"
            )

    for field, value in update_data.items():
        setattr(match, field, value)
    
    db.commit()
    db.refresh(match)
    return match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a match")
def delete_match(
    match_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """Delete a match by ID. Requires authentication."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    
    db.delete(match)
    db.commit()
    return None
