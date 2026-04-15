"""Tests for match CRUD endpoints."""

import pytest


class TestListMatches:
    """Test GET /matches/ endpoint."""

    def test_list_matches_with_data(self, client, sample_matches):
        """Test listing matches returns all matches."""
        response = client.get("/api/v1/matches/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    def test_list_matches_filter_by_season(self, client, sample_matches):
        """Test filtering matches by season."""
        response = client.get("/api/v1/matches/?season=2023-2024")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    def test_list_matches_filter_by_team(self, client, sample_matches, sample_teams):
        """Test filtering matches by team."""
        response = client.get(f"/api/v1/matches/?team_id={sample_teams[0].id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2  # Team Alpha plays in 2 matches


class TestCreateMatch:
    """Test POST /matches/ endpoint."""

    def test_create_match_success(self, client, auth_headers, sample_teams):
        """Test creating a new match."""
        response = client.post("/api/v1/matches/", json={
            "season": "2023-2024",
            "matchday": 4,
            "match_date": "2023-09-02",
            "home_team_id": sample_teams[0].id,
            "away_team_id": sample_teams[1].id,
            "home_goals": 1,
            "away_goals": 1,
        }, headers=auth_headers)
        assert response.status_code == 201

    def test_create_match_same_team(self, client, auth_headers, sample_teams):
        """Test creating a match with same home and away team returns 400."""
        response = client.post("/api/v1/matches/", json={
            "season": "2023-2024",
            "home_team_id": sample_teams[0].id,
            "away_team_id": sample_teams[0].id,
            "home_goals": 0,
            "away_goals": 0,
        }, headers=auth_headers)
        assert response.status_code == 400


class TestDeleteMatch:
    """Test DELETE /matches/{match_id} endpoint."""

    def test_delete_match_success(self, client, auth_headers, sample_matches):
        """Test deleting a match."""
        response = client.delete(f"/api/v1/matches/{sample_matches[0].id}", headers=auth_headers)
        assert response.status_code == 204
