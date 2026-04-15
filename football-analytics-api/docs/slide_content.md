# Football Analytics API - Oral Examination Presentation

## Slide 1: Title Slide
- **Title**: Football Analytics API: A Comprehensive Premier League Data Analysis Platform
- **Subtitle**: XJCO3011 - Web Services and Web Data | Coursework 1
- **Details**: Individual Web Services API Development Project | April 2026

---

## Slide 2: The API delivers real-time analysis of 380 Premier League matches across 20 teams
- The Football Analytics API is a RESTful web service built to manage and analyse Premier League football statistics from the 2023-2024 season.
- The dataset includes 20 Premier League clubs, 27 key players with detailed performance metrics, and 380 match records with comprehensive statistics (goals, possession, shots, fouls, attendance).
- The API provides 22 endpoints across 5 resource domains: Authentication, Teams, Players, Matches, and Analytics.
- Core functionality includes full CRUD operations, JWT-secured write access, advanced analytics (league tables, head-to-head comparisons), and auto-generated Swagger documentation.
- Target users: sports data analysts, application developers, and football enthusiasts seeking structured, queryable data.

---

## Slide 3: FastAPI + SQLAlchemy + SQLite delivers high performance with minimal infrastructure
- **Framework**: FastAPI was chosen for its async performance (benchmarks show 2-3x faster than Flask), native OpenAPI/Swagger documentation generation, and Pydantic-based type-safe validation.
- **Database**: SQLite provides zero-configuration setup with full SQL support. SQLAlchemy ORM abstracts database operations, preventing SQL injection and enabling clean relational modelling.
- **Authentication**: JWT tokens (python-jose) with bcrypt password hashing (passlib) provide stateless, industry-standard security. Public GET endpoints remain open; POST/PUT/DELETE require valid tokens.
- **Testing**: pytest with httpx TestClient enables isolated integration testing against an in-memory database. 45 tests cover all CRUD operations, authentication flows, analytics logic, and error handling.
- **Architecture**: Layered design separating Routers → Schemas → Models → Database, following separation of concerns and enabling independent testing of each layer.

---

## Slide 4: Layered architecture ensures clean separation of concerns across 5 modules
- The project follows a modular architecture with clear directory structure: `app/routers/` (HTTP handlers), `app/models/` (ORM entities), `app/schemas/` (validation), `app/services/` (business logic), `app/utils/` (authentication).
- **Database Schema**: Three core entities — Team (club details), Player (performance stats, FK to Team), Match (game statistics, FK to home/away Teams) — with a User entity for authentication.
- **API Versioning**: All endpoints are prefixed with `/api/v1/`, enabling future backward-compatible API evolution.
- **Middleware**: CORS middleware for cross-origin access, request timing middleware (X-Process-Time header), and global exception handling for consistent error responses.
- **Data Flow**: HTTP Request → Router (validation via Pydantic) → Service Logic → SQLAlchemy ORM → SQLite → JSON Response with proper HTTP status codes.

---

## Slide 5: Five analytics endpoints transform raw match data into actionable insights
- **League Table** (`/analytics/league-table`): Dynamically generates standings from match results, calculating points (W=3, D=1, L=0), goal difference, and last-5-match form. Sorted by points, then GD, then goals scored.
- **Team Performance** (`/analytics/team-performance/{id}`): Computes win rate, average goals scored/conceded, average possession, clean sheets, and separate home/away records for any team in any season.
- **Player Rankings** (`/analytics/player-rankings`): Ranks players by goals, assists, appearances, or market value with optional position and team filters. Returns top N results with team context.
- **Head-to-Head** (`/analytics/head-to-head`): Compares two teams' historical record, showing total wins, draws, goals, and individual match results with optional season filtering.
- **Season Summary** (`/analytics/season-summary`): Aggregates season-wide statistics including total goals, average goals per match, home/away win percentages, highest-scoring match, and top scorer/assister.

---

## Slide 6: Version control practices demonstrate consistent development workflow
- The GitHub repository maintains a clear commit history documenting the incremental development process from initial project setup through feature implementation to testing and documentation.
- **Commit Strategy**: Atomic commits grouped by feature (e.g., "Add team CRUD endpoints", "Implement JWT authentication", "Add league table analytics").
- **Repository Structure**: Clean separation between source code (`app/`), tests (`tests/`), documentation (`docs/`), and configuration files (`requirements.txt`, `README.md`).
- The README.md provides comprehensive setup instructions, API endpoint summary tables, authentication guide with demo credentials, and links to all deliverables.
- API documentation is available as both interactive Swagger UI (auto-generated at `/docs`) and a detailed PDF reference document in the `docs/` directory.

---

## Slide 7: 45 automated tests achieve comprehensive coverage across all endpoints
- **Test Architecture**: Uses pytest fixtures in `conftest.py` to create isolated test databases, sample data, and authentication tokens. Each test function receives a clean database state.
- **Authentication Tests** (7 tests): Cover successful registration, duplicate username/email detection, login with correct/incorrect credentials, and password validation.
- **CRUD Tests** (25 tests): Verify all Create, Read, Update, Delete operations for Teams, Players, and Matches, including pagination, filtering, sorting, and error handling (404, 401, 409).
- **Analytics Tests** (8 tests): Validate league table point calculations, team performance metrics, player ranking ordering, head-to-head aggregation, and season summary statistics.
- **Error Handling Tests** (5 tests): Confirm proper HTTP status codes for unauthorized access (401), resource not found (404), duplicate entries (409), and invalid input (422).

---

## Slide 8: Key challenges overcome and lessons learned during development
- **Challenge 1 — bcrypt Compatibility**: Encountered a `ValueError` due to incompatibility between `passlib` and `bcrypt>=4.1.0`. Resolved by pinning `bcrypt==4.0.1`, highlighting the importance of dependency management.
- **Challenge 2 — Complex Aggregation**: The league table endpoint required processing 380 matches to compute standings. Chose Python-based aggregation over complex SQL for readability and maintainability.
- **Challenge 3 — Test Isolation**: Initially, tests interfered with each other due to shared database state. Solved by implementing per-test database creation/teardown in fixtures.
- **Future Improvements**: Database migrations (Alembic), Redis caching for analytics, live data integration via external APIs (Sportmonks), and rate limiting for production deployment.
- **GenAI Usage (GREEN)**: AI was integral to code generation (80%), data seeding (100%), testing (90%), and documentation (70%). Human oversight was critical for architecture decisions, debugging, and quality assurance.

---

## Slide 9: Thank You and Q&A
- **Title**: Thank You — Questions Welcome
- **Summary**: The Football Analytics API demonstrates a production-quality RESTful service with 22 endpoints, JWT authentication, 5 analytics features, and 45 automated tests.
- **Key Links**: GitHub Repository | Swagger UI Documentation | Technical Report PDF
- **Contact**: Ready to discuss any technical decisions, implementation details, or future improvement plans.
