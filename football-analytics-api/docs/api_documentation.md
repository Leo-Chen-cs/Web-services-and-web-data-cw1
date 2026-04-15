# Football Analytics API Documentation

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000/api/v1`  
**Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)

---

## 1. Overview

The Football Analytics API provides a comprehensive set of RESTful endpoints for managing and analysing Premier League football data. The API supports full CRUD operations on three core data models (Teams, Players, Matches) and offers five advanced analytics endpoints for statistical analysis.

All responses are returned in **JSON** format. The API follows standard HTTP status codes and includes descriptive error messages for all failure cases.

---

## 2. Authentication

The API uses **JWT (JSON Web Token)** authentication based on the OAuth2 Bearer Token scheme.

**Public endpoints** (all GET requests) do not require authentication.  
**Protected endpoints** (POST, PUT, DELETE) require a valid JWT token in the `Authorization` header.

### 2.1 Register a New User

**Endpoint**: `POST /api/v1/auth/register`

**Request Body**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response** (201 Created):
```json
{
  "id": 3,
  "username": "newuser",
  "email": "user@example.com",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-15T10:30:00"
}
```

**Error Responses**:

| Status Code | Description |
|-------------|-------------|
| 409 Conflict | Username or email already registered |
| 422 Unprocessable Entity | Invalid input (e.g., password too short) |

### 2.2 Login

**Endpoint**: `POST /api/v1/auth/login`

**Request Body** (form-encoded):
```
username=admin&password=admin123
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Usage**: Include the token in subsequent requests:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Error Responses**:

| Status Code | Description |
|-------------|-------------|
| 401 Unauthorized | Incorrect username or password |
| 403 Forbidden | User account is deactivated |

---

## 3. Teams Endpoints

### 3.1 List Teams

**Endpoint**: `GET /api/v1/teams/`

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number (min: 1) |
| `page_size` | int | 20 | Items per page (1-100) |
| `search` | string | null | Search by team name (case-insensitive) |
| `league` | string | null | Filter by league |
| `city` | string | null | Filter by city |

**Example Request**:
```bash
GET /api/v1/teams/?page=1&page_size=5&search=Manchester
```

**Response** (200 OK):
```json
{
  "total": 2,
  "page": 1,
  "page_size": 5,
  "teams": [
    {
      "id": 1,
      "name": "Manchester City",
      "short_name": "MCI",
      "founded_year": 1880,
      "stadium": "Etihad Stadium",
      "city": "Manchester",
      "country": "England",
      "league": "Premier League",
      "manager": "Pep Guardiola",
      "budget_millions": 200.0,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": null
    }
  ]
}
```

### 3.2 Get Team by ID

**Endpoint**: `GET /api/v1/teams/{team_id}`

**Response** (200 OK): Single team object as shown above.

**Error**: 404 Not Found if team does not exist.

### 3.3 Create Team (Auth Required)

**Endpoint**: `POST /api/v1/teams/`

**Request Body**:
```json
{
  "name": "Leeds United",
  "short_name": "LEE",
  "city": "Leeds",
  "stadium": "Elland Road",
  "manager": "Daniel Farke",
  "budget_millions": 45.0
}
```

**Response** (201 Created): The created team object with assigned ID.

**Error Responses**:

| Status Code | Description |
|-------------|-------------|
| 401 Unauthorized | No valid authentication token |
| 409 Conflict | Team name already exists |
| 422 Unprocessable Entity | Invalid input data |

### 3.4 Update Team (Auth Required)

**Endpoint**: `PUT /api/v1/teams/{team_id}`

Supports partial updates - only include fields to be changed.

**Request Body**:
```json
{
  "manager": "New Manager",
  "budget_millions": 120.0
}
```

**Response** (200 OK): Updated team object.

### 3.5 Delete Team (Auth Required)

**Endpoint**: `DELETE /api/v1/teams/{team_id}`

**Response**: 204 No Content on success.

---

## 4. Players Endpoints

### 4.1 List Players

**Endpoint**: `GET /api/v1/players/`

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page (1-100) |
| `search` | string | null | Search by player name |
| `team_id` | int | null | Filter by team |
| `position` | string | null | Filter by position |
| `nationality` | string | null | Filter by nationality |
| `min_goals` | int | null | Minimum goals scored |
| `sort_by` | string | "name" | Sort field: name, goals, assists, appearances, market_value_millions |
| `sort_order` | string | "asc" | Sort order: asc or desc |

**Example Request**:
```bash
GET /api/v1/players/?sort_by=goals&sort_order=desc&position=Forward&page_size=5
```

**Response** (200 OK):
```json
{
  "total": 15,
  "page": 1,
  "page_size": 5,
  "players": [
    {
      "id": 1,
      "name": "Erling Haaland",
      "age": 23,
      "nationality": "Norway",
      "position": "Forward",
      "jersey_number": 9,
      "goals": 27,
      "assists": 5,
      "appearances": 31,
      "minutes_played": 2650,
      "yellow_cards": 3,
      "red_cards": 0,
      "market_value_millions": 180.0,
      "team_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": null
    }
  ]
}
```

### 4.2 Get Player by ID

**Endpoint**: `GET /api/v1/players/{player_id}`

### 4.3 Create Player (Auth Required)

**Endpoint**: `POST /api/v1/players/`

**Request Body**:
```json
{
  "name": "Jude Bellingham",
  "age": 20,
  "nationality": "England",
  "position": "Midfielder",
  "jersey_number": 5,
  "goals": 12,
  "assists": 8,
  "appearances": 28,
  "team_id": 1
}
```

### 4.4 Update Player (Auth Required)

**Endpoint**: `PUT /api/v1/players/{player_id}`

### 4.5 Delete Player (Auth Required)

**Endpoint**: `DELETE /api/v1/players/{player_id}`

---

## 5. Matches Endpoints

### 5.1 List Matches

**Endpoint**: `GET /api/v1/matches/`

**Query Parameters**:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page |
| `season` | string | null | Filter by season (e.g., "2023-2024") |
| `team_id` | int | null | Filter by team (home or away) |
| `date_from` | date | null | Filter from date (YYYY-MM-DD) |
| `date_to` | date | null | Filter to date (YYYY-MM-DD) |
| `matchday` | int | null | Filter by matchday |

**Example Request**:
```bash
GET /api/v1/matches/?season=2023-2024&team_id=1&page_size=3
```

**Response** (200 OK):
```json
{
  "total": 38,
  "page": 1,
  "page_size": 3,
  "matches": [
    {
      "id": 1,
      "season": "2023-2024",
      "matchday": 1,
      "match_date": "2023-08-14",
      "home_team_id": 1,
      "away_team_id": 2,
      "home_goals": 0,
      "away_goals": 2,
      "home_possession": 55.3,
      "away_possession": 44.7,
      "home_shots": 12,
      "away_shots": 8,
      "home_shots_on_target": 4,
      "away_shots_on_target": 5,
      "home_corners": 7,
      "away_corners": 3,
      "home_fouls": 10,
      "away_fouls": 12,
      "referee": "Michael Oliver",
      "venue": "Etihad Stadium",
      "attendance": 53400,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": null
    }
  ]
}
```

### 5.2 - 5.5 Get, Create, Update, Delete

Follow the same pattern as Teams and Players endpoints.

---

## 6. Analytics Endpoints

### 6.1 League Table

**Endpoint**: `GET /api/v1/analytics/league-table?season=2023-2024`

Generates a complete league standings table with points calculation (3 for win, 1 for draw, 0 for loss), goal difference, and recent form.

**Response** (200 OK):
```json
{
  "season": "2023-2024",
  "table": [
    {
      "position": 1,
      "team_id": 1,
      "team_name": "Manchester City",
      "played": 38,
      "won": 28,
      "drawn": 7,
      "lost": 3,
      "goals_for": 96,
      "goals_against": 34,
      "goal_difference": 62,
      "points": 91,
      "form": "WWDWW"
    }
  ]
}
```

### 6.2 Team Performance

**Endpoint**: `GET /api/v1/analytics/team-performance/{team_id}?season=2023-2024`

Returns detailed performance metrics including win rate, average goals, possession stats, clean sheets, and separate home/away records.

**Response** (200 OK):
```json
{
  "team_id": 1,
  "team_name": "Manchester City",
  "season": "2023-2024",
  "total_matches": 38,
  "wins": 28,
  "draws": 7,
  "losses": 3,
  "goals_scored": 96,
  "goals_conceded": 34,
  "goal_difference": 62,
  "points": 91,
  "win_rate": 73.7,
  "avg_goals_scored": 2.53,
  "avg_goals_conceded": 0.89,
  "avg_possession": 63.2,
  "avg_shots": 16.8,
  "clean_sheets": 18,
  "home_record": {"wins": 16, "draws": 2, "losses": 1},
  "away_record": {"wins": 12, "draws": 5, "losses": 2}
}
```

### 6.3 Player Rankings

**Endpoint**: `GET /api/v1/analytics/player-rankings?category=goals&limit=10`

**Query Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | **Required**. One of: `goals`, `assists`, `appearances`, `market_value` |
| `limit` | int | Number of players (default: 10, max: 50) |
| `position` | string | Optional position filter |
| `team_id` | int | Optional team filter |

**Response** (200 OK):
```json
{
  "category": "goals",
  "rankings": [
    {
      "rank": 1,
      "player_id": 1,
      "player_name": "Erling Haaland",
      "team_name": "Manchester City",
      "value": 27.0,
      "appearances": 31
    }
  ]
}
```

### 6.4 Head-to-Head Comparison

**Endpoint**: `GET /api/v1/analytics/head-to-head?team1_id=1&team2_id=2`

**Response** (200 OK):
```json
{
  "team1_id": 1,
  "team1_name": "Manchester City",
  "team2_id": 2,
  "team2_name": "Arsenal",
  "total_matches": 2,
  "team1_wins": 1,
  "team2_wins": 1,
  "draws": 0,
  "team1_goals": 3,
  "team2_goals": 4,
  "matches": [
    {
      "match_id": 1,
      "date": "2023-08-14",
      "home_team": "Manchester City",
      "away_team": "Arsenal",
      "home_goals": 0,
      "away_goals": 2,
      "result": "Arsenal Win"
    }
  ]
}
```

### 6.5 Season Summary

**Endpoint**: `GET /api/v1/analytics/season-summary?season=2023-2024`

**Response** (200 OK):
```json
{
  "season": "2023-2024",
  "total_matches": 380,
  "total_goals": 1115,
  "avg_goals_per_match": 2.93,
  "home_wins": 147,
  "away_wins": 144,
  "draws": 89,
  "home_win_percentage": 38.7,
  "most_goals_match": {
    "match_id": 14,
    "home_team": "Manchester City",
    "away_team": "Everton",
    "score": "3-3",
    "total_goals": 6
  },
  "top_scorer": {
    "player_id": 1,
    "name": "Erling Haaland",
    "goals": 27,
    "team": "Manchester City"
  },
  "top_assister": {
    "player_id": 6,
    "name": "Bukayo Saka",
    "assists": 13,
    "team": "Arsenal"
  }
}
```

---

## 7. Error Handling

All error responses follow a consistent format:

```json
{
  "detail": "Descriptive error message"
}
```

### Standard HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT requests |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input (e.g., same team for home/away) |
| 401 | Unauthorized | Missing or invalid authentication token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource does not exist |
| 409 | Conflict | Duplicate resource (e.g., team name) |
| 422 | Unprocessable Entity | Validation error in request body |
| 500 | Internal Server Error | Unexpected server error |

---

## 8. Data Models

### Team

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier (auto-generated) |
| name | string | Team full name (required, unique) |
| short_name | string | Short code (e.g., "MCI") |
| founded_year | integer | Year founded |
| stadium | string | Home stadium name |
| city | string | City location |
| country | string | Country (default: "England") |
| league | string | League name (default: "Premier League") |
| manager | string | Current manager |
| budget_millions | float | Transfer budget in millions |

### Player

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| name | string | Player full name (required) |
| age | integer | Player age (15-50) |
| nationality | string | Nationality |
| position | string | Playing position |
| jersey_number | integer | Shirt number (1-99) |
| goals | integer | Total goals scored |
| assists | integer | Total assists |
| appearances | integer | Total appearances |
| minutes_played | integer | Total minutes played |
| yellow_cards | integer | Yellow cards received |
| red_cards | integer | Red cards received |
| market_value_millions | float | Market value in millions |
| team_id | integer | Foreign key to Team |

### Match

| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier |
| season | string | Season (e.g., "2023-2024") |
| matchday | integer | Matchday number |
| match_date | date | Date of match |
| home_team_id | integer | Foreign key to home Team |
| away_team_id | integer | Foreign key to away Team |
| home_goals | integer | Home team goals |
| away_goals | integer | Away team goals |
| home_possession | float | Home possession % |
| away_possession | float | Away possession % |
| home_shots | integer | Home total shots |
| away_shots | integer | Away total shots |
| home_shots_on_target | integer | Home shots on target |
| away_shots_on_target | integer | Away shots on target |
| home_corners | integer | Home corner kicks |
| away_corners | integer | Away corner kicks |
| home_fouls | integer | Home fouls |
| away_fouls | integer | Away fouls |
| referee | string | Match referee |
| venue | string | Match venue |
| attendance | integer | Match attendance |
