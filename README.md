# Football Analytics API

A comprehensive RESTful API for Premier League football data analysis, built with **Python FastAPI**, **SQLAlchemy ORM**, and **SQLite**. This project provides full CRUD operations for teams, players, and matches, alongside advanced analytics endpoints including league tables, team performance metrics, player rankings, and head-to-head comparisons.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository](#repository)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Presentation Slides](#presentation-slides)
- [Authentication](#authentication)
- [API Endpoints Summary](#api-endpoints-summary)
- [Testing](#testing)
- [Data Sources](#data-sources)
- [Technical Report](#technical-report)

## Project Overview

The Football Analytics API is a data-driven web service designed to manage and analyse Premier League football statistics. It integrates a curated dataset of 20 Premier League teams, 27 key players, and 380 simulated match records for the 2023-2024 season. The API follows RESTful design principles and implements industry-standard authentication, error handling, and documentation practices.

### Core Data Model

- **Teams**: football clubs with metadata such as city, stadium, manager, and budget
- **Players**: footballers linked to teams, with position and performance statistics
- **Matches**: fixtures between two teams, including scorelines and match statistics
- **Users**: authenticated accounts for protected write operations

### Main Endpoint Groups

- `/api/v1/auth` for registration and JWT login
- `/api/v1/teams` for team CRUD operations
- `/api/v1/players` for player CRUD operations, filtering, and sorting
- `/api/v1/matches` for match CRUD operations and date/team filtering
- `/api/v1/analytics` for league tables, team performance, player rankings, head-to-head, and season summary

### Key Features

| Feature | Description |
|---------|-------------|
| **CRUD Operations** | Full Create, Read, Update, Delete for Teams, Players, and Matches |
| **JWT Authentication** | Secure token-based authentication with hash migration support and stronger input validation |
| **Advanced Analytics** | League tables, team performance, player rankings, head-to-head stats |
| **Pagination & Filtering** | All list endpoints support pagination, search, and multi-criteria filtering |
| **Swagger UI** | Auto-generated interactive API documentation |
| **Comprehensive Testing** | 78 automated tests covering auth, CRUD, analytics, validation, documentation, and regression edge cases |
| **Error Handling** | Consistent HTTP status codes with stricter validation for invalid query/update combinations |
| **Security Hardening** | Safer CORS defaults, secure response headers, and automatic password hash upgrades |

## Repository

- **Public GitHub Repository**: [https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1](https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1)
- **Main Branch**: [https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1/tree/main](https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1/tree/main)

This repository contains:

- Version-controlled source code with commit history
- `requirements.txt`
- API documentation PDF
- Technical report PDF
- Presentation slides in both PDF and PPTX format
- Automated test suite

## Technology Stack

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **Framework** | FastAPI 0.115 | High-performance async framework with automatic OpenAPI documentation |
| **ORM** | SQLAlchemy 2.0 | Industry-standard Python ORM with robust relationship management |
| **Database** | SQLite | Lightweight, zero-configuration SQL database ideal for development |
| **Authentication** | JWT (python-jose) | Stateless token-based auth following OAuth2 standards |
| **Password Hashing** | bcrypt (passlib) | Industry-standard adaptive hashing algorithm |
| **Validation** | Pydantic v2 | Type-safe request/response validation with automatic schema generation |
| **Testing** | pytest + httpx | Comprehensive test framework with async HTTP client support |

### Runtime Environment

- **Python Version**: Python 3.10+ recommended
- **Framework**: FastAPI
- **Database**: SQLite

## Project Structure

```
football-analytics-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point and configuration
│   ├── database.py             # Database engine and session management
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── team.py             # Team model
│   │   ├── player.py           # Player model
│   │   ├── match.py            # Match model
│   │   └── user.py             # User model for authentication
│   ├── schemas/                # Pydantic validation schemas
│   │   ├── __init__.py
│   │   ├── team.py             # Team request/response schemas
│   │   ├── player.py           # Player request/response schemas
│   │   ├── match.py            # Match request/response schemas
│   │   ├── user.py             # User and token schemas
│   │   └── analytics.py        # Analytics response schemas
│   ├── routers/                # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── teams.py            # Team CRUD endpoints
│   │   ├── players.py          # Player CRUD endpoints
│   │   ├── matches.py          # Match CRUD endpoints
│   │   └── analytics.py        # Analytics endpoints
│   ├── services/               # Business logic services
│   │   ├── __init__.py
│   │   └── seed_data.py        # Database seeding with sample data
│   └── utils/                  # Utility modules
│       ├── __init__.py
│       └── auth.py             # JWT and password utilities
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures and configuration
│   ├── test_auth.py            # Authentication tests
│   ├── test_teams.py           # Team CRUD tests
│   ├── test_players.py         # Player CRUD tests
│   ├── test_matches.py         # Match CRUD tests
│   └── test_analytics.py       # Analytics tests
├── data/                       # Database files
├── docs/                       # Documentation
│   └── api_documentation.pdf   # API documentation (PDF)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Setup and Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1.git
   cd Web-services-and-web-data-cw1
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the API:**
   - API Root: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

The database is automatically created and seeded with sample Premier League data on first startup.

## Running the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Interactive API documentation is available via:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive testing interface
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Clean reference documentation
- **API Documentation PDF**: [docs/api_documentation.pdf](https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1/blob/main/docs/api_documentation.pdf)
- **Rubric Self-Assessment**: [docs/xjco3011_self_assessment.md](docs/xjco3011_self_assessment.md)
- **GenAI Usage Appendix**: [docs/genai_usage_appendix.md](docs/genai_usage_appendix.md)

No public deployment URL is currently provided, so the local Swagger/ReDoc URLs above and the GitHub PDF are the primary documentation access points for marking.

## Presentation Slides

- **Slides PDF**: [Football_Analytics_API_-_Technical_Presentation.pdf](https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1/blob/main/docs/Football_Analytics_API_-_Technical_Presentation.pdf)
- **Slides PPTX**: [docs/Football_Analytics_API_-_Technical_Presentation.pptx](docs/Football_Analytics_API_-_Technical_Presentation.pptx)

## Authentication

The API uses **JWT (JSON Web Token)** authentication. Public read endpoints (GET) are accessible without authentication, while write operations (POST, PUT, DELETE) require a valid token.

### Quick Start

1. **Register** a new account:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "myuser", "email": "user@example.com", "password": "secure123"}'
   ```

2. **Login** to get a token:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -d "username=myuser&password=secure123"
   ```

3. **Use the token** in subsequent requests:
   ```bash
   curl -X POST http://localhost:8000/api/v1/teams/ \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "New Team FC"}'
   ```

### Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| User | `demo` | `demo123` |

## API Endpoints Summary

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |

### Teams (`/api/v1/teams`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| GET | `/teams/` | List all teams (paginated, filterable) | No |
| GET | `/teams/{id}` | Get team by ID | No |
| POST | `/teams/` | Create a new team | Yes |
| PUT | `/teams/{id}` | Update a team | Yes |
| DELETE | `/teams/{id}` | Delete a team | Yes |

### Players (`/api/v1/players`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| GET | `/players/` | List all players (paginated, filterable, sortable) | No |
| GET | `/players/{id}` | Get player by ID | No |
| POST | `/players/` | Create a new player | Yes |
| PUT | `/players/{id}` | Update a player | Yes |
| DELETE | `/players/{id}` | Delete a player | Yes |

### Matches (`/api/v1/matches`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| GET | `/matches/` | List all matches (paginated, filterable) | No |
| GET | `/matches/{id}` | Get match by ID | No |
| POST | `/matches/` | Create a new match | Yes |
| PUT | `/matches/{id}` | Update a match | Yes |
| DELETE | `/matches/{id}` | Delete a match | Yes |

### Analytics (`/api/v1/analytics`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|:---:|
| GET | `/analytics/league-table` | Generate league standings | No |
| GET | `/analytics/team-performance/{id}` | Detailed team metrics | No |
| GET | `/analytics/player-rankings` | Player rankings by category | No |
| GET | `/analytics/head-to-head` | Head-to-head comparison | No |
| GET | `/analytics/season-summary` | Season-wide statistics | No |

## Testing

Run the complete test suite:

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ -v --tb=short

# Run specific test file
python -m pytest tests/test_teams.py -v
```

**Test Results**: 78 tests passing, covering authentication, CRUD operations, analytics, validation, documentation availability, error handling, and regression edge cases.

## Data Sources

The API is pre-seeded with data inspired by the **Premier League 2023-2024 season**. Team information, player statistics, and match data are based on publicly available football statistics from sources including:

- [Premier League Official Website](https://www.premierleague.com/)
- [Football-Data.co.uk](https://www.football-data.co.uk/)
- [Kaggle Football Datasets](https://www.kaggle.com/datasets)

## Technical Report

- **Technical Report PDF**: [docs/technical_report.pdf](https://github.com/Leo-Chen-cs/Web-services-and-web-data-cw1/blob/main/docs/technical_report.pdf)

The full technical report covers:

- Architecture and design decisions
- Technology stack justification
- Testing methodology
- Challenges and lessons learned
- Generative AI declaration

## GenAI Statement

Generative AI was used in a declared and limited support role for debugging, validation hardening, test expansion, and documentation refinement. A fuller disclosure is provided in the technical report and in [docs/genai_usage_appendix.md](docs/genai_usage_appendix.md).

---

**Module**: XJCO3011 - Web Services and Web Data  
**Assessment**: Coursework 1 - Individual Web Services API Development Project  
**Academic Year**: 2025-2026
