"""Pydantic schemas for Team endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Team name")
    short_name: Optional[str] = Field(None, max_length=10, description="Short name / abbreviation")
    founded_year: Optional[int] = Field(None, ge=1800, le=2026, description="Year the club was founded")
    stadium: Optional[str] = Field(None, max_length=100, description="Home stadium name")
    city: Optional[str] = Field(None, max_length=50, description="City")
    country: Optional[str] = Field("England", max_length=50, description="Country")
    league: Optional[str] = Field("Premier League", max_length=50, description="League name")
    manager: Optional[str] = Field(None, max_length=100, description="Current manager")
    budget_millions: Optional[float] = Field(None, ge=0, description="Transfer budget in millions")


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, max_length=10)
    founded_year: Optional[int] = Field(None, ge=1800, le=2026)
    stadium: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=50)
    country: Optional[str] = Field(None, max_length=50)
    league: Optional[str] = Field(None, max_length=50)
    manager: Optional[str] = Field(None, max_length=100)
    budget_millions: Optional[float] = Field(None, ge=0)


class TeamResponse(TeamBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TeamListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    teams: List[TeamResponse]
