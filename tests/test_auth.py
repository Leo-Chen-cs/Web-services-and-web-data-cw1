"""Tests for authentication endpoints."""

import pytest

from app.models.user import User
from app.utils.auth import create_access_token, get_password_hash


class TestRegister:
    """Test user registration endpoint."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "hashed_password" not in data

    def test_register_duplicate_username(self, client, sample_user):
        """Test registration with duplicate username returns 409."""
        response = client.post("/api/v1/auth/register", json={
            "username": "testuser",
            "email": "different@example.com",
            "password": "password123",
        })
        assert response.status_code == 409

    def test_register_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email returns 409."""
        response = client.post("/api/v1/auth/register", json={
            "username": "differentuser",
            "email": "test@example.com",
            "password": "password123",
        })
        assert response.status_code == 409

    def test_register_short_password(self, client):
        """Test registration with too short password returns 422."""
        response = client.post("/api/v1/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "short",
        })
        assert response.status_code == 422

    def test_register_password_requires_letters_and_numbers(self, client):
        """Test registration rejects weak passwords without digits."""
        response = client.post("/api/v1/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "passwordonly",
        })
        assert response.status_code == 422

    def test_register_invalid_username(self, client):
        """Test registration rejects usernames with unsupported characters."""
        response = client.post("/api/v1/auth/register", json={
            "username": "bad user!",
            "email": "new@example.com",
            "password": "password123",
        })
        assert response.status_code == 422

    def test_register_invalid_email(self, client):
        """Test registration rejects malformed email addresses."""
        response = client.post("/api/v1/auth/register", json={
            "username": "newuser",
            "email": "not-an-email",
            "password": "password123",
        })
        assert response.status_code == 422


class TestLogin:
    """Test user login endpoint."""

    def test_login_success(self, client, sample_user):
        """Test successful login returns JWT token."""
        response = client.post("/api/v1/auth/login", data={
            "username": "testuser",
            "password": "testpass123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, sample_user):
        """Test login with wrong password returns 401."""
        response = client.post("/api/v1/auth/login", data={
            "username": "testuser",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user returns 401."""
        response = client.post("/api/v1/auth/login", data={
            "username": "nonexistent",
            "password": "password123",
        })
        assert response.status_code == 401

    def test_login_rehashes_legacy_password_hash(self, client, db_session):
        """Test successful login upgrades legacy bcrypt hashes."""
        user = User(
            username="legacyuser",
            email="legacy@example.com",
            hashed_password="$2b$12$abqR.Lz1GMgZooA7Sqa4o.b4sI/Ky4N..IhhN45ySDTEeHprgYKGa",
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()

        response = client.post("/api/v1/auth/login", data={
            "username": "legacyuser",
            "password": "legacypass1",
        })
        assert response.status_code == 200

        db_session.refresh(user)
        assert user.hashed_password.startswith("$pbkdf2-sha256$")

    def test_login_inactive_user_forbidden(self, client, db_session):
        """Test inactive users cannot log in."""
        user = User(
            username="inactiveuser",
            email="inactive@example.com",
            hashed_password=get_password_hash("inactive123"),
            is_active=False,
        )
        db_session.add(user)
        db_session.commit()

        response = client.post("/api/v1/auth/login", data={
            "username": "inactiveuser",
            "password": "inactive123",
        })
        assert response.status_code == 403

    def test_inactive_user_token_rejected_on_protected_endpoint(self, client, db_session):
        """Test inactive users cannot keep using protected endpoints via old tokens."""
        user = User(
            username="disabledwriter",
            email="disabled@example.com",
            hashed_password=get_password_hash("inactive123"),
            is_active=False,
        )
        db_session.add(user)
        db_session.commit()

        token = create_access_token(data={"sub": user.username})
        response = client.post("/api/v1/teams/", json={
            "name": "Blocked Team",
        }, headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403
