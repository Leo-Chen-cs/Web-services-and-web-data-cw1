"""
Test configuration and fixtures.
Uses a separate in-memory SQLite database for test isolation.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.models.team import Team
from app.models.player import Player
from app.models.match import Match
from app.utils.auth import get_password_hash, create_access_token
from datetime import date

# Test database - in-memory SQLite
TEST_DATABASE_URL = "sqlite:///./data/test_football.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    """Create an admin user for testing."""
    user = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass123"),
        is_admin=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(sample_user):
    """Generate authentication headers for testing."""
    token = create_access_token(data={"sub": sample_user.username})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(admin_user):
    """Generate admin authentication headers for testing."""
    token = create_access_token(data={"sub": admin_user.username})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_teams(db_session):
    """Create sample teams for testing."""
    teams = [
        Team(name="Team Alpha", short_name="ALP", city="London", stadium="Alpha Stadium", manager="Coach A", budget_millions=100.0),
        Team(name="Team Beta", short_name="BET", city="Manchester", stadium="Beta Stadium", manager="Coach B", budget_millions=80.0),
        Team(name="Team Gamma", short_name="GAM", city="Liverpool", stadium="Gamma Stadium", manager="Coach C", budget_millions=60.0),
    ]
    for t in teams:
        db_session.add(t)
    db_session.commit()
    for t in teams:
        db_session.refresh(t)
    return teams


@pytest.fixture
def sample_players(db_session, sample_teams):
    """Create sample players for testing."""
    players = [
        Player(name="Player One", age=25, nationality="England", position="Forward", jersey_number=9, goals=15, assists=8, appearances=30, team_id=sample_teams[0].id),
        Player(name="Player Two", age=28, nationality="Spain", position="Midfielder", jersey_number=10, goals=8, assists=12, appearances=32, team_id=sample_teams[0].id),
        Player(name="Player Three", age=22, nationality="Brazil", position="Defender", jersey_number=4, goals=2, assists=3, appearances=28, team_id=sample_teams[1].id),
    ]
    for p in players:
        db_session.add(p)
    db_session.commit()
    for p in players:
        db_session.refresh(p)
    return players


@pytest.fixture
def sample_matches(db_session, sample_teams):
    """Create sample matches for testing."""
    matches = [
        Match(season="2023-2024", matchday=1, match_date=date(2023, 8, 12), home_team_id=sample_teams[0].id, away_team_id=sample_teams[1].id, home_goals=2, away_goals=1, home_possession=55.0, away_possession=45.0, home_shots=12, away_shots=8, venue="Alpha Stadium"),
        Match(season="2023-2024", matchday=2, match_date=date(2023, 8, 19), home_team_id=sample_teams[1].id, away_team_id=sample_teams[2].id, home_goals=0, away_goals=0, home_possession=48.0, away_possession=52.0, home_shots=6, away_shots=9, venue="Beta Stadium"),
        Match(season="2023-2024", matchday=3, match_date=date(2023, 8, 26), home_team_id=sample_teams[2].id, away_team_id=sample_teams[0].id, home_goals=1, away_goals=3, home_possession=40.0, away_possession=60.0, home_shots=7, away_shots=15, venue="Gamma Stadium"),
    ]
    for m in matches:
        db_session.add(m)
    db_session.commit()
    for m in matches:
        db_session.refresh(m)
    return matches
