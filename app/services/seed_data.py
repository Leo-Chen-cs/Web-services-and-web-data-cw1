"""
Seed data service.
Populates the database with realistic Premier League data for the 2023-2024 season.
Data sourced from publicly available football statistics.
"""

from sqlalchemy.orm import Session
from app.models.team import Team
from app.models.player import Player
from app.models.match import Match
from app.models.user import User
from app.utils.auth import get_password_hash
from datetime import date
import random

# Premier League 2023-2024 teams with realistic data
TEAMS_DATA = [
    {"name": "Manchester City", "short_name": "MCI", "founded_year": 1880, "stadium": "Etihad Stadium", "city": "Manchester", "manager": "Pep Guardiola", "budget_millions": 200.0},
    {"name": "Arsenal", "short_name": "ARS", "founded_year": 1886, "stadium": "Emirates Stadium", "city": "London", "manager": "Mikel Arteta", "budget_millions": 180.0},
    {"name": "Liverpool", "short_name": "LIV", "founded_year": 1892, "stadium": "Anfield", "city": "Liverpool", "manager": "Jurgen Klopp", "budget_millions": 170.0},
    {"name": "Aston Villa", "short_name": "AVL", "founded_year": 1874, "stadium": "Villa Park", "city": "Birmingham", "manager": "Unai Emery", "budget_millions": 120.0},
    {"name": "Tottenham Hotspur", "short_name": "TOT", "founded_year": 1882, "stadium": "Tottenham Hotspur Stadium", "city": "London", "manager": "Ange Postecoglou", "budget_millions": 150.0},
    {"name": "Chelsea", "short_name": "CHE", "founded_year": 1905, "stadium": "Stamford Bridge", "city": "London", "manager": "Mauricio Pochettino", "budget_millions": 250.0},
    {"name": "Newcastle United", "short_name": "NEW", "founded_year": 1892, "stadium": "St James' Park", "city": "Newcastle", "manager": "Eddie Howe", "budget_millions": 160.0},
    {"name": "Manchester United", "short_name": "MUN", "founded_year": 1878, "stadium": "Old Trafford", "city": "Manchester", "manager": "Erik ten Hag", "budget_millions": 190.0},
    {"name": "West Ham United", "short_name": "WHU", "founded_year": 1895, "stadium": "London Stadium", "city": "London", "manager": "David Moyes", "budget_millions": 100.0},
    {"name": "Brighton & Hove Albion", "short_name": "BHA", "founded_year": 1901, "stadium": "Amex Stadium", "city": "Brighton", "manager": "Roberto De Zerbi", "budget_millions": 90.0},
    {"name": "Wolverhampton Wanderers", "short_name": "WOL", "founded_year": 1877, "stadium": "Molineux Stadium", "city": "Wolverhampton", "manager": "Gary O'Neil", "budget_millions": 80.0},
    {"name": "Crystal Palace", "short_name": "CRY", "founded_year": 1905, "stadium": "Selhurst Park", "city": "London", "manager": "Roy Hodgson", "budget_millions": 70.0},
    {"name": "Bournemouth", "short_name": "BOU", "founded_year": 1899, "stadium": "Vitality Stadium", "city": "Bournemouth", "manager": "Andoni Iraola", "budget_millions": 60.0},
    {"name": "Fulham", "short_name": "FUL", "founded_year": 1879, "stadium": "Craven Cottage", "city": "London", "manager": "Marco Silva", "budget_millions": 65.0},
    {"name": "Everton", "short_name": "EVE", "founded_year": 1878, "stadium": "Goodison Park", "city": "Liverpool", "manager": "Sean Dyche", "budget_millions": 55.0},
    {"name": "Brentford", "short_name": "BRE", "founded_year": 1889, "stadium": "Gtech Community Stadium", "city": "London", "manager": "Thomas Frank", "budget_millions": 50.0},
    {"name": "Nottingham Forest", "short_name": "NFO", "founded_year": 1865, "stadium": "City Ground", "city": "Nottingham", "manager": "Nuno Espirito Santo", "budget_millions": 75.0},
    {"name": "Luton Town", "short_name": "LUT", "founded_year": 1885, "stadium": "Kenilworth Road", "city": "Luton", "manager": "Rob Edwards", "budget_millions": 30.0},
    {"name": "Burnley", "short_name": "BUR", "founded_year": 1882, "stadium": "Turf Moor", "city": "Burnley", "manager": "Vincent Kompany", "budget_millions": 35.0},
    {"name": "Sheffield United", "short_name": "SHU", "founded_year": 1889, "stadium": "Bramall Lane", "city": "Sheffield", "manager": "Chris Wilder", "budget_millions": 25.0},
]

# Sample players data (key players from each team)
PLAYERS_DATA = {
    "Manchester City": [
        {"name": "Erling Haaland", "age": 23, "nationality": "Norway", "position": "Forward", "jersey_number": 9, "goals": 27, "assists": 5, "appearances": 31, "minutes_played": 2650, "yellow_cards": 3, "red_cards": 0, "market_value_millions": 180.0},
        {"name": "Kevin De Bruyne", "age": 32, "nationality": "Belgium", "position": "Midfielder", "jersey_number": 17, "goals": 4, "assists": 10, "appearances": 18, "minutes_played": 1350, "yellow_cards": 2, "red_cards": 0, "market_value_millions": 75.0},
        {"name": "Phil Foden", "age": 23, "nationality": "England", "position": "Midfielder", "jersey_number": 47, "goals": 19, "assists": 8, "appearances": 35, "minutes_played": 2800, "yellow_cards": 4, "red_cards": 0, "market_value_millions": 130.0},
        {"name": "Rodri", "age": 27, "nationality": "Spain", "position": "Midfielder", "jersey_number": 16, "goals": 8, "assists": 9, "appearances": 34, "minutes_played": 2950, "yellow_cards": 7, "red_cards": 0, "market_value_millions": 120.0},
        {"name": "Ederson", "age": 30, "nationality": "Brazil", "position": "Goalkeeper", "jersey_number": 31, "goals": 0, "assists": 1, "appearances": 33, "minutes_played": 2970, "yellow_cards": 1, "red_cards": 0, "market_value_millions": 40.0},
    ],
    "Arsenal": [
        {"name": "Bukayo Saka", "age": 22, "nationality": "England", "position": "Forward", "jersey_number": 7, "goals": 16, "assists": 13, "appearances": 35, "minutes_played": 2900, "yellow_cards": 5, "red_cards": 0, "market_value_millions": 140.0},
        {"name": "Martin Odegaard", "age": 25, "nationality": "Norway", "position": "Midfielder", "jersey_number": 8, "goals": 8, "assists": 10, "appearances": 33, "minutes_played": 2750, "yellow_cards": 3, "red_cards": 0, "market_value_millions": 120.0},
        {"name": "Kai Havertz", "age": 24, "nationality": "Germany", "position": "Forward", "jersey_number": 29, "goals": 13, "assists": 7, "appearances": 37, "minutes_played": 2600, "yellow_cards": 6, "red_cards": 0, "market_value_millions": 65.0},
        {"name": "Declan Rice", "age": 25, "nationality": "England", "position": "Midfielder", "jersey_number": 41, "goals": 7, "assists": 8, "appearances": 38, "minutes_played": 3300, "yellow_cards": 8, "red_cards": 0, "market_value_millions": 110.0},
        {"name": "William Saliba", "age": 23, "nationality": "France", "position": "Defender", "jersey_number": 12, "goals": 2, "assists": 1, "appearances": 35, "minutes_played": 3100, "yellow_cards": 4, "red_cards": 0, "market_value_millions": 90.0},
    ],
    "Liverpool": [
        {"name": "Mohamed Salah", "age": 31, "nationality": "Egypt", "position": "Forward", "jersey_number": 11, "goals": 18, "assists": 10, "appearances": 32, "minutes_played": 2700, "yellow_cards": 1, "red_cards": 0, "market_value_millions": 80.0},
        {"name": "Virgil van Dijk", "age": 32, "nationality": "Netherlands", "position": "Defender", "jersey_number": 4, "goals": 2, "assists": 2, "appearances": 33, "minutes_played": 2950, "yellow_cards": 3, "red_cards": 0, "market_value_millions": 35.0},
        {"name": "Darwin Nunez", "age": 24, "nationality": "Uruguay", "position": "Forward", "jersey_number": 9, "goals": 11, "assists": 8, "appearances": 36, "minutes_played": 2200, "yellow_cards": 5, "red_cards": 1, "market_value_millions": 70.0},
        {"name": "Alexis Mac Allister", "age": 25, "nationality": "Argentina", "position": "Midfielder", "jersey_number": 10, "goals": 5, "assists": 7, "appearances": 36, "minutes_played": 2900, "yellow_cards": 6, "red_cards": 0, "market_value_millions": 80.0},
        {"name": "Alisson Becker", "age": 31, "nationality": "Brazil", "position": "Goalkeeper", "jersey_number": 1, "goals": 0, "assists": 1, "appearances": 32, "minutes_played": 2880, "yellow_cards": 0, "red_cards": 0, "market_value_millions": 35.0},
    ],
    "Aston Villa": [
        {"name": "Ollie Watkins", "age": 28, "nationality": "England", "position": "Forward", "jersey_number": 11, "goals": 19, "assists": 13, "appearances": 37, "minutes_played": 3200, "yellow_cards": 4, "red_cards": 0, "market_value_millions": 55.0},
        {"name": "Leon Bailey", "age": 26, "nationality": "Jamaica", "position": "Forward", "jersey_number": 31, "goals": 10, "assists": 9, "appearances": 33, "minutes_played": 2100, "yellow_cards": 3, "red_cards": 0, "market_value_millions": 30.0},
    ],
    "Tottenham Hotspur": [
        {"name": "Son Heung-min", "age": 31, "nationality": "South Korea", "position": "Forward", "jersey_number": 7, "goals": 17, "assists": 10, "appearances": 35, "minutes_played": 2900, "yellow_cards": 2, "red_cards": 0, "market_value_millions": 60.0},
        {"name": "James Maddison", "age": 27, "nationality": "England", "position": "Midfielder", "jersey_number": 10, "goals": 4, "assists": 9, "appearances": 28, "minutes_played": 2100, "yellow_cards": 5, "red_cards": 0, "market_value_millions": 50.0},
    ],
    "Chelsea": [
        {"name": "Cole Palmer", "age": 21, "nationality": "England", "position": "Forward", "jersey_number": 20, "goals": 22, "assists": 11, "appearances": 34, "minutes_played": 2800, "yellow_cards": 2, "red_cards": 0, "market_value_millions": 100.0},
        {"name": "Nicolas Jackson", "age": 22, "nationality": "Senegal", "position": "Forward", "jersey_number": 15, "goals": 14, "assists": 5, "appearances": 35, "minutes_played": 2600, "yellow_cards": 4, "red_cards": 0, "market_value_millions": 45.0},
    ],
    "Newcastle United": [
        {"name": "Alexander Isak", "age": 24, "nationality": "Sweden", "position": "Forward", "jersey_number": 14, "goals": 21, "assists": 3, "appearances": 30, "minutes_played": 2500, "yellow_cards": 2, "red_cards": 0, "market_value_millions": 90.0},
        {"name": "Bruno Guimaraes", "age": 26, "nationality": "Brazil", "position": "Midfielder", "jersey_number": 39, "goals": 7, "assists": 8, "appearances": 37, "minutes_played": 3100, "yellow_cards": 9, "red_cards": 0, "market_value_millions": 80.0},
    ],
    "Manchester United": [
        {"name": "Bruno Fernandes", "age": 29, "nationality": "Portugal", "position": "Midfielder", "jersey_number": 8, "goals": 10, "assists": 8, "appearances": 35, "minutes_played": 3050, "yellow_cards": 7, "red_cards": 0, "market_value_millions": 70.0},
        {"name": "Rasmus Hojlund", "age": 21, "nationality": "Denmark", "position": "Forward", "jersey_number": 11, "goals": 10, "assists": 2, "appearances": 30, "minutes_played": 2200, "yellow_cards": 3, "red_cards": 0, "market_value_millions": 50.0},
    ],
    "West Ham United": [
        {"name": "Jarrod Bowen", "age": 27, "nationality": "England", "position": "Forward", "jersey_number": 20, "goals": 16, "assists": 6, "appearances": 37, "minutes_played": 3100, "yellow_cards": 3, "red_cards": 0, "market_value_millions": 45.0},
    ],
    "Brighton & Hove Albion": [
        {"name": "Joao Pedro", "age": 22, "nationality": "Brazil", "position": "Forward", "jersey_number": 9, "goals": 9, "assists": 4, "appearances": 33, "minutes_played": 2400, "yellow_cards": 4, "red_cards": 0, "market_value_millions": 35.0},
    ],
}

# Referees
REFEREES = ["Michael Oliver", "Anthony Taylor", "Paul Tierney", "Simon Hooper", "Robert Jones", "Craig Pawson", "Andy Madley", "David Coote", "John Brooks", "Stuart Attwell"]


def generate_match_stats():
    """Generate realistic match statistics."""
    home_poss = round(random.uniform(35, 70), 1)
    return {
        "home_possession": home_poss,
        "away_possession": round(100 - home_poss, 1),
        "home_shots": random.randint(5, 25),
        "away_shots": random.randint(3, 22),
        "home_shots_on_target": random.randint(1, 12),
        "away_shots_on_target": random.randint(0, 10),
        "home_corners": random.randint(1, 14),
        "away_corners": random.randint(0, 12),
        "home_fouls": random.randint(5, 18),
        "away_fouls": random.randint(4, 17),
        "referee": random.choice(REFEREES),
        "attendance": random.randint(20000, 75000),
    }


def seed_database(db: Session):
    """Populate database with sample data."""
    # Check if data already exists
    if db.query(Team).count() > 0:
        return False
    
    # Create demo user
    demo_user = User(
        username="admin",
        email="admin@footballapi.com",
        hashed_password=get_password_hash("admin123"),
        is_admin=True,
    )
    db.add(demo_user)
    
    demo_user2 = User(
        username="demo",
        email="demo@footballapi.com",
        hashed_password=get_password_hash("demo123"),
        is_admin=False,
    )
    db.add(demo_user2)
    
    # Create teams
    team_objects = {}
    for team_data in TEAMS_DATA:
        team = Team(**team_data, country="England", league="Premier League")
        db.add(team)
        db.flush()
        team_objects[team.name] = team
    
    # Create players
    for team_name, players in PLAYERS_DATA.items():
        team = team_objects[team_name]
        for player_data in players:
            player = Player(**player_data, team_id=team.id)
            db.add(player)
    
    # Generate matches for 2023-2024 season (round-robin)
    team_list = list(team_objects.values())
    random.seed(42)  # Reproducible results
    
    matchday = 0
    base_date = date(2023, 8, 12)
    
    # Generate all home-away combinations (each team plays every other team once at home)
    for i, home_team in enumerate(team_list):
        for j, away_team in enumerate(team_list):
            if i == j:
                continue
            
            matchday += 1
            day_offset = (matchday // 10) * 7 + random.randint(0, 2)
            match_date = date(2023, 8, 12)
            
            # Calculate date
            month = 8 + (day_offset // 30)
            day = 12 + (day_offset % 28)
            if month > 12:
                year = 2024
                month -= 12
            else:
                year = 2023
            
            try:
                match_date = date(year, min(month, 12), min(day, 28))
            except ValueError:
                match_date = date(2024, 1, 15)
            
            # Generate realistic scores based on team strength
            strength_diff = i - j  # Lower index = stronger team
            home_advantage = 0.5
            
            if strength_diff < -5:
                home_goals = random.choices([0, 1, 2, 3, 4], weights=[15, 25, 30, 20, 10])[0]
                away_goals = random.choices([0, 1, 2, 3], weights=[30, 35, 25, 10])[0]
            elif strength_diff > 5:
                home_goals = random.choices([0, 1, 2], weights=[30, 40, 30])[0]
                away_goals = random.choices([0, 1, 2, 3, 4], weights=[15, 25, 30, 20, 10])[0]
            else:
                home_goals = random.choices([0, 1, 2, 3], weights=[20, 35, 30, 15])[0]
                away_goals = random.choices([0, 1, 2, 3], weights=[25, 35, 25, 15])[0]
            
            stats = generate_match_stats()
            
            match = Match(
                season="2023-2024",
                matchday=(matchday % 38) + 1,
                match_date=match_date,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                home_goals=home_goals,
                away_goals=away_goals,
                venue=home_team.stadium,
                **stats,
            )
            db.add(match)
    
    db.commit()
    return True
