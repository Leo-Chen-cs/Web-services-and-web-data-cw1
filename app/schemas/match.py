"""Pydantic schemas for Match endpoints."""

from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MatchBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    season: str = Field(..., min_length=1, max_length=20, description="Season identifier, e.g. 2023-2024")
    matchday: Optional[int] = Field(None, ge=1, le=50, description="Matchday number")
    match_date: Optional[date] = Field(None, description="Date of the match")
    home_team_id: int = Field(..., description="Home team ID")
    away_team_id: int = Field(..., description="Away team ID")
    home_goals: int = Field(..., ge=0, description="Goals scored by home team")
    away_goals: int = Field(..., ge=0, description="Goals scored by away team")
    home_possession: Optional[float] = Field(None, ge=0, le=100, description="Home possession %")
    away_possession: Optional[float] = Field(None, ge=0, le=100, description="Away possession %")
    home_shots: Optional[int] = Field(None, ge=0, description="Home total shots")
    away_shots: Optional[int] = Field(None, ge=0, description="Away total shots")
    home_shots_on_target: Optional[int] = Field(None, ge=0, description="Home shots on target")
    away_shots_on_target: Optional[int] = Field(None, ge=0, description="Away shots on target")
    home_corners: Optional[int] = Field(None, ge=0, description="Home corner kicks")
    away_corners: Optional[int] = Field(None, ge=0, description="Away corner kicks")
    home_fouls: Optional[int] = Field(None, ge=0, description="Home fouls committed")
    away_fouls: Optional[int] = Field(None, ge=0, description="Away fouls committed")
    referee: Optional[str] = Field(None, max_length=100, description="Match referee")
    venue: Optional[str] = Field(None, max_length=100, description="Match venue")
    attendance: Optional[int] = Field(None, ge=0, description="Match attendance")

    @model_validator(mode="after")
    def validate_match_consistency(self):
        if (
            self.home_possession is not None
            and self.away_possession is not None
            and abs((self.home_possession + self.away_possession) - 100) > 1
        ):
            raise ValueError("Home and away possession must total approximately 100")
        if (
            self.home_shots is not None
            and self.home_shots_on_target is not None
            and self.home_shots_on_target > self.home_shots
        ):
            raise ValueError("Home shots on target cannot exceed total shots")
        if (
            self.away_shots is not None
            and self.away_shots_on_target is not None
            and self.away_shots_on_target > self.away_shots
        ):
            raise ValueError("Away shots on target cannot exceed total shots")
        return self


class MatchCreate(MatchBase):
    pass


class MatchUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    season: Optional[str] = Field(None, min_length=1, max_length=20)
    matchday: Optional[int] = Field(None, ge=1, le=50)
    match_date: Optional[date] = None
    home_team_id: Optional[int] = None
    away_team_id: Optional[int] = None
    home_goals: Optional[int] = Field(None, ge=0)
    away_goals: Optional[int] = Field(None, ge=0)
    home_possession: Optional[float] = Field(None, ge=0, le=100)
    away_possession: Optional[float] = Field(None, ge=0, le=100)
    home_shots: Optional[int] = Field(None, ge=0)
    away_shots: Optional[int] = Field(None, ge=0)
    home_shots_on_target: Optional[int] = Field(None, ge=0)
    away_shots_on_target: Optional[int] = Field(None, ge=0)
    home_corners: Optional[int] = Field(None, ge=0)
    away_corners: Optional[int] = Field(None, ge=0)
    home_fouls: Optional[int] = Field(None, ge=0)
    away_fouls: Optional[int] = Field(None, ge=0)
    referee: Optional[str] = Field(None, max_length=100)
    venue: Optional[str] = Field(None, max_length=100)
    attendance: Optional[int] = Field(None, ge=0)

    @model_validator(mode="after")
    def validate_match_consistency(self):
        if (
            self.home_possession is not None
            and self.away_possession is not None
            and abs((self.home_possession + self.away_possession) - 100) > 1
        ):
            raise ValueError("Home and away possession must total approximately 100")
        if (
            self.home_shots is not None
            and self.home_shots_on_target is not None
            and self.home_shots_on_target > self.home_shots
        ):
            raise ValueError("Home shots on target cannot exceed total shots")
        if (
            self.away_shots is not None
            and self.away_shots_on_target is not None
            and self.away_shots_on_target > self.away_shots
        ):
            raise ValueError("Away shots on target cannot exceed total shots")
        return self


class MatchResponse(MatchBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class MatchListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    matches: List[MatchResponse]
