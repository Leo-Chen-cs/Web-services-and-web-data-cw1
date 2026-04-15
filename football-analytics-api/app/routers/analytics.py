"""
Analytics endpoints.
Provides advanced data analysis features including league tables,
team performance metrics, player rankings, head-to-head comparisons,
and season summaries.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case, or_, and_
from typing import Optional
from app.database import get_db
from app.models.match import Match
from app.models.team import Team
from app.models.player import Player
from app.schemas.analytics import (
    LeagueTableEntry, LeagueTableResponse,
    TeamPerformanceResponse,
    PlayerRankingEntry, PlayerRankingResponse,
    HeadToHeadMatch, HeadToHeadResponse,
    SeasonSummaryResponse,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/league-table", response_model=LeagueTableResponse, summary="Get league table")
def get_league_table(
    season: str = Query(..., description="Season identifier, e.g. 2023-2024"),
    db: Session = Depends(get_db),
):
    """
    Generate a complete league table for a given season.
    
    Calculates points (3 for win, 1 for draw, 0 for loss), goal difference,
    and ranks teams accordingly. Includes recent form (last 5 matches).
    """
    teams = db.query(Team).all()
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")
    
    matches = db.query(Match).filter(Match.season == season).all()
    if not matches:
        raise HTTPException(status_code=404, detail=f"No matches found for season {season}")
    
    # Build table
    table_data = {}
    team_matches = {}  # Track match results for form
    
    for team in teams:
        table_data[team.id] = {
            "team_id": team.id,
            "team_name": team.name,
            "played": 0, "won": 0, "drawn": 0, "lost": 0,
            "goals_for": 0, "goals_against": 0,
        }
        team_matches[team.id] = []
    
    for match in sorted(matches, key=lambda m: m.match_date or ""):
        hid, aid = match.home_team_id, match.away_team_id
        
        if hid not in table_data or aid not in table_data:
            continue
        
        table_data[hid]["played"] += 1
        table_data[aid]["played"] += 1
        table_data[hid]["goals_for"] += match.home_goals
        table_data[hid]["goals_against"] += match.away_goals
        table_data[aid]["goals_for"] += match.away_goals
        table_data[aid]["goals_against"] += match.home_goals
        
        if match.home_goals > match.away_goals:
            table_data[hid]["won"] += 1
            table_data[aid]["lost"] += 1
            team_matches[hid].append("W")
            team_matches[aid].append("L")
        elif match.home_goals < match.away_goals:
            table_data[aid]["won"] += 1
            table_data[hid]["lost"] += 1
            team_matches[aid].append("W")
            team_matches[hid].append("L")
        else:
            table_data[hid]["drawn"] += 1
            table_data[aid]["drawn"] += 1
            team_matches[hid].append("D")
            team_matches[aid].append("D")
    
    # Calculate points and goal difference, build entries
    entries = []
    for tid, data in table_data.items():
        if data["played"] == 0:
            continue
        gd = data["goals_for"] - data["goals_against"]
        pts = data["won"] * 3 + data["drawn"]
        form = "".join(team_matches[tid][-5:]) if team_matches[tid] else ""
        entries.append(LeagueTableEntry(
            position=0,
            team_id=data["team_id"],
            team_name=data["team_name"],
            played=data["played"],
            won=data["won"],
            drawn=data["drawn"],
            lost=data["lost"],
            goals_for=data["goals_for"],
            goals_against=data["goals_against"],
            goal_difference=gd,
            points=pts,
            form=form,
        ))
    
    # Sort: points desc, goal_difference desc, goals_for desc
    entries.sort(key=lambda e: (-e.points, -e.goal_difference, -e.goals_for))
    for i, entry in enumerate(entries):
        entry.position = i + 1
    
    return LeagueTableResponse(season=season, table=entries)


@router.get("/team-performance/{team_id}", response_model=TeamPerformanceResponse, summary="Get team performance")
def get_team_performance(
    team_id: int,
    season: str = Query(..., description="Season identifier"),
    db: Session = Depends(get_db),
):
    """
    Get detailed performance metrics for a specific team in a given season.
    
    Includes win rate, average goals, possession stats, clean sheets,
    and separate home/away records.
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail=f"Team with id {team_id} not found")
    
    matches = db.query(Match).filter(
        Match.season == season,
        or_(Match.home_team_id == team_id, Match.away_team_id == team_id)
    ).all()
    
    if not matches:
        raise HTTPException(status_code=404, detail=f"No matches found for team {team_id} in season {season}")
    
    wins = draws = losses = 0
    goals_scored = goals_conceded = 0
    clean_sheets = 0
    total_possession = 0
    total_shots = 0
    possession_count = 0
    shots_count = 0
    home_record = {"wins": 0, "draws": 0, "losses": 0}
    away_record = {"wins": 0, "draws": 0, "losses": 0}
    
    for m in matches:
        is_home = m.home_team_id == team_id
        gf = m.home_goals if is_home else m.away_goals
        ga = m.away_goals if is_home else m.home_goals
        
        goals_scored += gf
        goals_conceded += ga
        
        if ga == 0:
            clean_sheets += 1
        
        poss = m.home_possession if is_home else m.away_possession
        shots = m.home_shots if is_home else m.away_shots
        
        if poss is not None:
            total_possession += poss
            possession_count += 1
        if shots is not None:
            total_shots += shots
            shots_count += 1
        
        record = home_record if is_home else away_record
        if gf > ga:
            wins += 1
            record["wins"] += 1
        elif gf < ga:
            losses += 1
            record["losses"] += 1
        else:
            draws += 1
            record["draws"] += 1
    
    total = len(matches)
    
    return TeamPerformanceResponse(
        team_id=team_id,
        team_name=team.name,
        season=season,
        total_matches=total,
        wins=wins,
        draws=draws,
        losses=losses,
        goals_scored=goals_scored,
        goals_conceded=goals_conceded,
        goal_difference=goals_scored - goals_conceded,
        points=wins * 3 + draws,
        win_rate=round(wins / total * 100, 1) if total > 0 else 0,
        avg_goals_scored=round(goals_scored / total, 2) if total > 0 else 0,
        avg_goals_conceded=round(goals_conceded / total, 2) if total > 0 else 0,
        avg_possession=round(total_possession / possession_count, 1) if possession_count > 0 else None,
        avg_shots=round(total_shots / shots_count, 1) if shots_count > 0 else None,
        clean_sheets=clean_sheets,
        home_record=home_record,
        away_record=away_record,
    )


@router.get("/player-rankings", response_model=PlayerRankingResponse, summary="Get player rankings")
def get_player_rankings(
    category: str = Query(..., description="Ranking category: goals, assists, appearances, market_value"),
    limit: int = Query(10, ge=1, le=50, description="Number of players to return"),
    position: Optional[str] = Query(None, description="Filter by position"),
    team_id: Optional[int] = Query(None, description="Filter by team"),
    db: Session = Depends(get_db),
):
    """
    Get player rankings by various statistical categories.
    
    Available categories:
    - **goals**: Top scorers
    - **assists**: Top assist providers
    - **appearances**: Most appearances
    - **market_value**: Highest market value
    """
    category_map = {
        "goals": Player.goals,
        "assists": Player.assists,
        "appearances": Player.appearances,
        "market_value": Player.market_value_millions,
    }
    
    if category not in category_map:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Choose from: {', '.join(category_map.keys())}"
        )
    
    query = db.query(Player).join(Team)
    
    if position:
        query = query.filter(Player.position.ilike(f"%{position}%"))
    if team_id:
        query = query.filter(Player.team_id == team_id)
    
    sort_col = category_map[category]
    players = query.order_by(sort_col.desc()).limit(limit).all()
    
    rankings = []
    for i, p in enumerate(players):
        value = getattr(p, category if category != "market_value" else "market_value_millions") or 0
        rankings.append(PlayerRankingEntry(
            rank=i + 1,
            player_id=p.id,
            player_name=p.name,
            team_name=p.team.name if p.team else "Unknown",
            value=float(value),
            appearances=p.appearances or 0,
        ))
    
    return PlayerRankingResponse(category=category, rankings=rankings)


@router.get("/head-to-head", response_model=HeadToHeadResponse, summary="Head-to-head comparison")
def get_head_to_head(
    team1_id: int = Query(..., description="First team ID"),
    team2_id: int = Query(..., description="Second team ID"),
    season: Optional[str] = Query(None, description="Optional season filter"),
    db: Session = Depends(get_db),
):
    """
    Get head-to-head statistics between two teams.
    
    Returns historical match results, win counts, and total goals
    for both teams across all or a specific season.
    """
    team1 = db.query(Team).filter(Team.id == team1_id).first()
    team2 = db.query(Team).filter(Team.id == team2_id).first()
    
    if not team1 or not team2:
        raise HTTPException(status_code=404, detail="One or both teams not found")
    
    query = db.query(Match).filter(
        or_(
            and_(Match.home_team_id == team1_id, Match.away_team_id == team2_id),
            and_(Match.home_team_id == team2_id, Match.away_team_id == team1_id),
        )
    )
    
    if season:
        query = query.filter(Match.season == season)
    
    matches = query.order_by(Match.match_date.desc()).all()
    
    t1_wins = t2_wins = draws = t1_goals = t2_goals = 0
    match_list = []
    
    for m in matches:
        if m.home_team_id == team1_id:
            g1, g2 = m.home_goals, m.away_goals
        else:
            g1, g2 = m.away_goals, m.home_goals
        
        t1_goals += g1
        t2_goals += g2
        
        if g1 > g2:
            t1_wins += 1
            result = f"{team1.name} Win"
        elif g2 > g1:
            t2_wins += 1
            result = f"{team2.name} Win"
        else:
            draws += 1
            result = "Draw"
        
        match_list.append(HeadToHeadMatch(
            match_id=m.id,
            date=str(m.match_date) if m.match_date else None,
            home_team=team1.name if m.home_team_id == team1_id else team2.name,
            away_team=team2.name if m.home_team_id == team1_id else team1.name,
            home_goals=m.home_goals,
            away_goals=m.away_goals,
            result=result,
        ))
    
    return HeadToHeadResponse(
        team1_id=team1_id,
        team1_name=team1.name,
        team2_id=team2_id,
        team2_name=team2.name,
        total_matches=len(matches),
        team1_wins=t1_wins,
        team2_wins=t2_wins,
        draws=draws,
        team1_goals=t1_goals,
        team2_goals=t2_goals,
        matches=match_list,
    )


@router.get("/season-summary", response_model=SeasonSummaryResponse, summary="Get season summary")
def get_season_summary(
    season: str = Query(..., description="Season identifier"),
    db: Session = Depends(get_db),
):
    """
    Get a comprehensive summary of an entire season.
    
    Includes total matches, goals, averages, home/away win percentages,
    the highest-scoring match, and top scorer/assister.
    """
    matches = db.query(Match).filter(Match.season == season).all()
    if not matches:
        raise HTTPException(status_code=404, detail=f"No matches found for season {season}")
    
    total_matches = len(matches)
    total_goals = sum(m.home_goals + m.away_goals for m in matches)
    home_wins = sum(1 for m in matches if m.home_goals > m.away_goals)
    away_wins = sum(1 for m in matches if m.away_goals > m.home_goals)
    draws = sum(1 for m in matches if m.home_goals == m.away_goals)
    
    # Find highest scoring match
    most_goals_match = max(matches, key=lambda m: m.home_goals + m.away_goals)
    home_t = db.query(Team).filter(Team.id == most_goals_match.home_team_id).first()
    away_t = db.query(Team).filter(Team.id == most_goals_match.away_team_id).first()
    
    most_goals_info = {
        "match_id": most_goals_match.id,
        "home_team": home_t.name if home_t else "Unknown",
        "away_team": away_t.name if away_t else "Unknown",
        "score": f"{most_goals_match.home_goals}-{most_goals_match.away_goals}",
        "total_goals": most_goals_match.home_goals + most_goals_match.away_goals,
    }
    
    # Top scorer
    top_scorer_player = db.query(Player).order_by(Player.goals.desc()).first()
    top_scorer = None
    if top_scorer_player:
        top_scorer = {
            "player_id": top_scorer_player.id,
            "name": top_scorer_player.name,
            "goals": top_scorer_player.goals,
            "team": top_scorer_player.team.name if top_scorer_player.team else "Unknown",
        }
    
    # Top assister
    top_assister_player = db.query(Player).order_by(Player.assists.desc()).first()
    top_assister = None
    if top_assister_player:
        top_assister = {
            "player_id": top_assister_player.id,
            "name": top_assister_player.name,
            "assists": top_assister_player.assists,
            "team": top_assister_player.team.name if top_assister_player.team else "Unknown",
        }
    
    return SeasonSummaryResponse(
        season=season,
        total_matches=total_matches,
        total_goals=total_goals,
        avg_goals_per_match=round(total_goals / total_matches, 2),
        home_wins=home_wins,
        away_wins=away_wins,
        draws=draws,
        home_win_percentage=round(home_wins / total_matches * 100, 1),
        most_goals_match=most_goals_info,
        top_scorer=top_scorer,
        top_assister=top_assister,
    )
