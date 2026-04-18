"""Tests for team CRUD endpoints."""

import pytest


class TestListTeams:
    """Test GET /teams/ endpoint."""

    def test_list_teams_empty(self, client):
        """Test listing teams when database is empty."""
        response = client.get("/api/v1/teams/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["teams"] == []

    def test_list_teams_with_data(self, client, sample_teams):
        """Test listing teams returns all teams."""
        response = client.get("/api/v1/teams/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["teams"]) == 3

    def test_list_teams_pagination(self, client, sample_teams):
        """Test pagination works correctly."""
        response = client.get("/api/v1/teams/?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 3
        assert len(data["teams"]) == 2
        assert data["page"] == 1

    def test_list_teams_search(self, client, sample_teams):
        """Test search filtering by name."""
        response = client.get("/api/v1/teams/?search=Alpha")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["teams"][0]["name"] == "Team Alpha"

    def test_list_teams_filter_city(self, client, sample_teams):
        """Test filtering by city."""
        response = client.get("/api/v1/teams/?city=London")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1


class TestGetTeam:
    """Test GET /teams/{team_id} endpoint."""

    def test_get_team_success(self, client, sample_teams):
        """Test getting a specific team by ID."""
        response = client.get(f"/api/v1/teams/{sample_teams[0].id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Team Alpha"

    def test_get_team_not_found(self, client):
        """Test getting a non-existent team returns 404."""
        response = client.get("/api/v1/teams/999")
        assert response.status_code == 404


class TestCreateTeam:
    """Test POST /teams/ endpoint."""

    def test_create_team_success(self, client, auth_headers):
        """Test creating a new team with authentication."""
        response = client.post("/api/v1/teams/", json={
            "name": "New Team FC",
            "short_name": "NTF",
            "city": "Leeds",
            "stadium": "New Stadium",
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Team FC"
        assert data["id"] is not None

    def test_create_team_unauthorized(self, client):
        """Test creating a team without auth returns 401."""
        response = client.post("/api/v1/teams/", json={
            "name": "Unauthorized FC",
        })
        assert response.status_code == 401

    def test_create_team_duplicate(self, client, auth_headers, sample_teams):
        """Test creating a team with duplicate name returns 409."""
        response = client.post("/api/v1/teams/", json={
            "name": "Team Alpha",
        }, headers=auth_headers)
        assert response.status_code == 409


class TestUpdateTeam:
    """Test PUT /teams/{team_id} endpoint."""

    def test_update_team_success(self, client, auth_headers, sample_teams):
        """Test updating a team."""
        response = client.put(f"/api/v1/teams/{sample_teams[0].id}", json={
            "manager": "New Manager",
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["manager"] == "New Manager"

    def test_update_team_not_found(self, client, auth_headers):
        """Test updating a non-existent team returns 404."""
        response = client.put("/api/v1/teams/999", json={
            "name": "Updated",
        }, headers=auth_headers)
        assert response.status_code == 404

    def test_update_team_duplicate_name(self, client, auth_headers, sample_teams):
        """Test renaming a team to an existing name returns 409."""
        response = client.put(f"/api/v1/teams/{sample_teams[1].id}", json={
            "name": sample_teams[0].name,
        }, headers=auth_headers)
        assert response.status_code == 409


class TestDeleteTeam:
    """Test DELETE /teams/{team_id} endpoint."""

    def test_delete_team_success(self, client, auth_headers, sample_teams):
        """Test deleting a team."""
        response = client.delete(f"/api/v1/teams/{sample_teams[0].id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify deletion
        response = client.get(f"/api/v1/teams/{sample_teams[0].id}")
        assert response.status_code == 404

    def test_delete_team_not_found(self, client, auth_headers):
        """Test deleting a non-existent team returns 404."""
        response = client.delete("/api/v1/teams/999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_team_unauthorized(self, client, sample_teams):
        """Test deleting without auth returns 401."""
        response = client.delete(f"/api/v1/teams/{sample_teams[0].id}")
        assert response.status_code == 401
