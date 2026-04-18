"""Pydantic schemas for Player endpoints."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

VALID_POSITIONS = {"Goalkeeper", "Defender", "Midfielder", "Forward"}


class PlayerBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=100, description="Player full name")
    age: Optional[int] = Field(None, ge=15, le=50, description="Player age")
    nationality: Optional[str] = Field(None, max_length=50, description="Nationality")
    position: Optional[str] = Field(None, description="Playing position")
    jersey_number: Optional[int] = Field(None, ge=1, le=99, description="Jersey number")
    goals: Optional[int] = Field(0, ge=0, description="Total goals scored")
    assists: Optional[int] = Field(0, ge=0, description="Total assists")
    appearances: Optional[int] = Field(0, ge=0, description="Total appearances")
    minutes_played: Optional[int] = Field(0, ge=0, description="Total minutes played")
    yellow_cards: Optional[int] = Field(0, ge=0, description="Yellow cards received")
    red_cards: Optional[int] = Field(0, ge=0, description="Red cards received")
    market_value_millions: Optional[float] = Field(None, ge=0, description="Market value in millions")
    team_id: int = Field(..., description="ID of the team the player belongs to")

    @field_validator("position")
    @classmethod
    def validate_position(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        if value not in VALID_POSITIONS:
            raise ValueError(f"Position must be one of: {', '.join(sorted(VALID_POSITIONS))}")
        return value


class PlayerCreate(PlayerBase):
    pass


class PlayerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=15, le=50)
    nationality: Optional[str] = Field(None, max_length=50)
    position: Optional[str] = Field(None)
    jersey_number: Optional[int] = Field(None, ge=1, le=99)
    goals: Optional[int] = Field(None, ge=0)
    assists: Optional[int] = Field(None, ge=0)
    appearances: Optional[int] = Field(None, ge=0)
    minutes_played: Optional[int] = Field(None, ge=0)
    yellow_cards: Optional[int] = Field(None, ge=0)
    red_cards: Optional[int] = Field(None, ge=0)
    market_value_millions: Optional[float] = Field(None, ge=0)
    team_id: Optional[int] = Field(None)


class PlayerResponse(PlayerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PlayerListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    players: List[PlayerResponse]
