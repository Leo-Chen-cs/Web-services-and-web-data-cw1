"""
Player CRUD endpoints.
Provides full Create, Read, Update, Delete operations for football players.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.player import Player
from app.models.team import Team
from app.schemas.player import PlayerCreate, PlayerUpdate, PlayerResponse, PlayerListResponse
from app.utils.auth import require_auth
from app.models.user import User

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/", response_model=PlayerListResponse, summary="List all players")
def list_players(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by player name"),
    team_id: Optional[int] = Query(None, description="Filter by team ID"),
    position: Optional[str] = Query(None, description="Filter by position"),
    nationality: Optional[str] = Query(None, description="Filter by nationality"),
    min_goals: Optional[int] = Query(None, ge=0, description="Minimum goals"),
    sort_by: Optional[str] = Query("name", description="Sort field: name, goals, assists, appearances, market_value_millions"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    db: Session = Depends(get_db),
):
    """
    Retrieve a paginated list of players with optional filtering and sorting.
    
    Supports multiple filter criteria and sorting options for flexible queries.
    """
    query = db.query(Player)
    
    if search:
        query = query.filter(Player.name.ilike(f"%{search}%"))
    if team_id:
        query = query.filter(Player.team_id == team_id)
    if position:
        query = query.filter(Player.position.ilike(f"%{position}%"))
    if nationality:
        query = query.filter(Player.nationality.ilike(f"%{nationality}%"))
    if min_goals is not None:
        query = query.filter(Player.goals >= min_goals)
    
    # Sorting
    sort_column = getattr(Player, sort_by, Player.name)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    total = query.count()
    players = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return PlayerListResponse(
        total=total,
        page=page,
        page_size=page_size,
        players=players
    )


@router.get("/{player_id}", response_model=PlayerResponse, summary="Get player by ID")
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific player by their ID."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found"
        )
    return player


@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED, summary="Create a new player")
def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Create a new player. Requires authentication.
    
    The team_id must reference an existing team.
    """
    # Validate team exists
    team = db.query(Team).filter(Team.id == player_data.team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id {player_data.team_id} not found"
        )
    
    player = Player(**player_data.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@router.put("/{player_id}", response_model=PlayerResponse, summary="Update a player")
def update_player(
    player_id: int,
    player_data: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """
    Update an existing player. Requires authentication.
    
    Only provided fields will be updated (partial update supported).
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found"
        )
    
    update_data = player_data.model_dump(exclude_unset=True)
    
    # Validate team_id if being updated
    if "team_id" in update_data:
        team = db.query(Team).filter(Team.id == update_data["team_id"]).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team with id {update_data['team_id']} not found"
            )
    
    for field, value in update_data.items():
        setattr(player, field, value)
    
    db.commit()
    db.refresh(player)
    return player


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a player")
def delete_player(
    player_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_auth),
):
    """Delete a player by ID. Requires authentication."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found"
        )
    
    db.delete(player)
    db.commit()
    return None
