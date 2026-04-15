"""Pydantic schemas for analytics endpoints."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class LeagueTableEntry(BaseModel):
    position: int
    team_id: int
    team_name: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    form: Optional[str] = Field(None, description="Last 5 results, e.g. WWDLW")


class LeagueTableResponse(BaseModel):
    season: str
    table: List[LeagueTableEntry]


class TeamPerformanceResponse(BaseModel):
    team_id: int
    team_name: str
    season: str
    total_matches: int
    wins: int
    draws: int
    losses: int
    goals_scored: int
    goals_conceded: int
    goal_difference: int
    points: int
    win_rate: float
    avg_goals_scored: float
    avg_goals_conceded: float
    avg_possession: Optional[float] = None
    avg_shots: Optional[float] = None
    clean_sheets: int
    home_record: Dict[str, int]
    away_record: Dict[str, int]


class PlayerRankingEntry(BaseModel):
    rank: int
    player_id: int
    player_name: str
    team_name: str
    value: float
    appearances: int


class PlayerRankingResponse(BaseModel):
    category: str
    season: Optional[str] = None
    rankings: List[PlayerRankingEntry]


class HeadToHeadMatch(BaseModel):
    match_id: int
    date: Optional[str] = None
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int
    result: str


class HeadToHeadResponse(BaseModel):
    team1_id: int
    team1_name: str
    team2_id: int
    team2_name: str
    total_matches: int
    team1_wins: int
    team2_wins: int
    draws: int
    team1_goals: int
    team2_goals: int
    matches: List[HeadToHeadMatch]


class SeasonSummaryResponse(BaseModel):
    season: str
    total_matches: int
    total_goals: int
    avg_goals_per_match: float
    home_wins: int
    away_wins: int
    draws: int
    home_win_percentage: float
    most_goals_match: Optional[Dict] = None
    top_scorer: Optional[Dict] = None
    top_assister: Optional[Dict] = None
