"""Tests for player CRUD endpoints."""

import pytest


class TestListPlayers:
    """Test GET /players/ endpoint."""

    def test_list_players_with_data(self, client, sample_players):
        """Test listing players returns all players."""
        response = client.get("/api/v1/players/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3

    def test_list_players_filter_by_team(self, client, sample_players, sample_teams):
        """Test filtering players by team."""
        response = client.get(f"/api/v1/players/?team_id={sample_teams[0].id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2

    def test_list_players_filter_by_position(self, client, sample_players):
        """Test filtering players by position."""
        response = client.get("/api/v1/players/?position=Forward")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1

    def test_list_players_sort_by_goals(self, client, sample_players):
        """Test sorting players by goals descending."""
        response = client.get("/api/v1/players/?sort_by=goals&sort_order=desc")
        assert response.status_code == 200
        data = response.json()
        assert data["players"][0]["goals"] >= data["players"][1]["goals"]

    def test_list_players_invalid_sort_field(self, client, sample_players):
        """Test invalid sort fields return 400 instead of silently falling back."""
        response = client.get("/api/v1/players/?sort_by=unknown_field")
        assert response.status_code == 400


class TestCreatePlayer:
    """Test POST /players/ endpoint."""

    def test_create_player_success(self, client, auth_headers, sample_teams):
        """Test creating a new player."""
        response = client.post("/api/v1/players/", json={
            "name": "New Player",
            "age": 24,
            "nationality": "France",
            "position": "Midfielder",
            "team_id": sample_teams[0].id,
        }, headers=auth_headers)
        assert response.status_code == 201
        assert response.json()["name"] == "New Player"

    def test_create_player_invalid_team(self, client, auth_headers):
        """Test creating a player with invalid team returns 404."""
        response = client.post("/api/v1/players/", json={
            "name": "Orphan Player",
            "team_id": 999,
        }, headers=auth_headers)
        assert response.status_code == 404


class TestUpdatePlayer:
    """Test PUT /players/{player_id} endpoint."""

    def test_update_player_success(self, client, auth_headers, sample_players):
        """Test updating a player's stats."""
        response = client.put(f"/api/v1/players/{sample_players[0].id}", json={
            "goals": 20,
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["goals"] == 20


class TestDeletePlayer:
    """Test DELETE /players/{player_id} endpoint."""

    def test_delete_player_success(self, client, auth_headers, sample_players):
        """Test deleting a player."""
        response = client.delete(f"/api/v1/players/{sample_players[0].id}", headers=auth_headers)
        assert response.status_code == 204
