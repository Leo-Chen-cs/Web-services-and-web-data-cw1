"""
Team CRUD endpoints.
Provides full Create, Read, Update, Delete operations for football teams.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate, TeamResponse, TeamListResponse
from app.utils.auth import get_current_user, require_auth
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["Teams"])


@router.get("/", response_model=TeamListResponse, summary="List all teams")
def list_teams(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by team name"),
    league: Optional[str] = Query(None, description="Filter by league"),
    city: Optional[str] = Query(None, description="Filter by city"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of teams with optional filtering.
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    - **search**: Optional search term for team name (case-insensitive)
    - **league**: Optional filter by league name
    - **city**: Optional filter by city
    """
    query = db.query(Team)
    
    if search:
        query = query.filter(Team.name.ilike(f"%{search}%"))
    if league:
        query = query.filter(Team.league == league)
    if city:
        query = query.filter(Team.city.ilike(f"%{city}%"))
    query = query.order_by(Team.name.asc())
    
    total = query.count()
    teams = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return TeamListResponse(
        total=total,
        page=page,
        page_size=page_size,
        teams=teams
    )


@router.get("/{team_id}", response_model=TeamResponse, summary="Get team by ID")
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific team by its ID."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found"
        )
    return team


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED, summary="Create a new team")
def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Create a new team. Requires authentication.
    
    Returns the created team with its assigned ID.
    """
    # Check for duplicate name
    existing = db.query(Team).filter(Team.name == team_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Team with name '{team_data.name}' already exists"
        )
    
    team = Team(**team_data.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.put("/{team_id}", response_model=TeamResponse, summary="Update a team")
def update_team(
    team_id: int,
    team_data: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Update an existing team. Requires authentication.
    
    Only provided fields will be updated (partial update supported).
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found"
        )
    
    update_data = team_data.model_dump(exclude_unset=True)

    if "name" in update_data:
        existing = (
            db.query(Team)
            .filter(func.lower(Team.name) == update_data["name"].lower(), Team.id != team_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Team with name '{update_data['name']}' already exists"
            )

    for field, value in update_data.items():
        setattr(team, field, value)
    
    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a team")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Delete a team by ID. Requires authentication.
    
    This will also cascade-delete all associated players.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {team_id} not found"
        )
    
    db.delete(team)
    db.commit()
    return None
