"""Tests for analytics endpoints."""

import pytest


class TestLeagueTable:
    """Test GET /analytics/league-table endpoint."""

    def test_league_table_success(self, client, sample_matches):
        """Test generating a league table for a season."""
        response = client.get("/api/v1/analytics/league-table?season=2023-2024")
        assert response.status_code == 200
        data = response.json()
        assert data["season"] == "2023-2024"
        assert len(data["table"]) > 0
        # Verify positions are assigned
        assert data["table"][0]["position"] == 1
        # Verify points calculation (3 for win, 1 for draw)
        for entry in data["table"]:
            expected_points = entry["won"] * 3 + entry["drawn"]
            assert entry["points"] == expected_points

    def test_league_table_no_matches(self, client, sample_teams):
        """Test league table with no matches returns 404."""
        response = client.get("/api/v1/analytics/league-table?season=2099-2100")
        assert response.status_code == 404


class TestTeamPerformance:
    """Test GET /analytics/team-performance/{team_id} endpoint."""

    def test_team_performance_success(self, client, sample_matches, sample_teams):
        """Test getting team performance metrics."""
        response = client.get(f"/api/v1/analytics/team-performance/{sample_teams[0].id}?season=2023-2024")
        assert response.status_code == 200
        data = response.json()
        assert data["team_id"] == sample_teams[0].id
        assert data["total_matches"] == 2
        assert "win_rate" in data
        assert "home_record" in data
        assert "away_record" in data

    def test_team_performance_not_found(self, client):
        """Test team performance for non-existent team returns 404."""
        response = client.get("/api/v1/analytics/team-performance/999?season=2023-2024")
        assert response.status_code == 404


class TestPlayerRankings:
    """Test GET /analytics/player-rankings endpoint."""

    def test_player_rankings_goals(self, client, sample_players):
        """Test player rankings by goals."""
        response = client.get("/api/v1/analytics/player-rankings?category=goals&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert data["category"] == "goals"
        assert len(data["rankings"]) > 0
        # Verify descending order
        values = [r["value"] for r in data["rankings"]]
        assert values == sorted(values, reverse=True)

    def test_player_rankings_invalid_category(self, client):
        """Test player rankings with invalid category returns 400."""
        response = client.get("/api/v1/analytics/player-rankings?category=invalid")
        assert response.status_code == 400


class TestHeadToHead:
    """Test GET /analytics/head-to-head endpoint."""

    def test_head_to_head_success(self, client, sample_matches, sample_teams):
        """Test head-to-head comparison between two teams."""
        response = client.get(f"/api/v1/analytics/head-to-head?team1_id={sample_teams[0].id}&team2_id={sample_teams[1].id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total_matches"] > 0
        assert data["team1_wins"] + data["team2_wins"] + data["draws"] == data["total_matches"]


class TestSeasonSummary:
    """Test GET /analytics/season-summary endpoint."""

    def test_season_summary_success(self, client, sample_matches):
        """Test getting season summary."""
        response = client.get("/api/v1/analytics/season-summary?season=2023-2024")
        assert response.status_code == 200
        data = response.json()
        assert data["season"] == "2023-2024"
        assert data["total_matches"] == 3
        assert data["total_goals"] > 0
        assert data["home_wins"] + data["away_wins"] + data["draws"] == data["total_matches"]

    def test_season_summary_not_found(self, client):
        """Test season summary for non-existent season returns 404."""
        response = client.get("/api/v1/analytics/season-summary?season=2099-2100")
        assert response.status_code == 404
