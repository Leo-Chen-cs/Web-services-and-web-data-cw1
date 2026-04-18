"""
Football Analytics API - Main Application Entry Point

A comprehensive RESTful API for Premier League football data analysis.
Built with FastAPI, SQLAlchemy, and SQLite.

Features:
- Full CRUD operations for Teams, Players, and Matches
- JWT-based authentication
- Advanced analytics endpoints (league tables, performance metrics, rankings)
- Swagger UI documentation
- Comprehensive error handling
"""

from contextlib import asynccontextmanager
import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import init_db, SessionLocal
from app.routers import teams, players, matches, auth, analytics
from app.services.seed_data import seed_database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_allowed_origins() -> list[str]:
    """Read allowed CORS origins from env or use safe local defaults."""
    raw_origins = os.getenv(
        "CORS_ALLOW_ORIGINS",
        "http://localhost,http://localhost:3000,http://127.0.0.1,http://127.0.0.1:3000",
    )
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - initializes database on startup."""
    logger.info("Initializing database...")
    init_db()
    
    # Seed with sample data
    db = SessionLocal()
    try:
        if seed_database(db):
            logger.info("Database seeded with sample Premier League data")
        else:
            logger.info("Database already contains data, skipping seed")
    finally:
        db.close()
    
    yield
    logger.info("Application shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Football Analytics API",
    description="""
## Premier League Football Analytics API

A fully functional data-driven web API for analysing Premier League football data.
This API provides comprehensive endpoints for managing and analysing teams, players,
and match statistics from the 2023-2024 season.

### Features
- **Teams**: Full CRUD operations for football clubs
- **Players**: Full CRUD operations with advanced filtering and sorting
- **Matches**: Full CRUD operations with date range and team filtering
- **Analytics**: League tables, team performance, player rankings, head-to-head comparisons
- **Authentication**: JWT-based security for write operations

### Authentication
Public endpoints (GET) are accessible without authentication.
Write operations (POST, PUT, DELETE) require a valid JWT token.

To authenticate:
1. Register a new account via `/api/v1/auth/register`
2. Login via `/api/v1/auth/login` to receive a JWT token
3. Include the token in the `Authorization: Bearer <token>` header

### Demo Credentials
- **Admin**: username=`admin`, password=`admin123`
- **User**: username=`demo`, password=`demo123`
    """,
    version="1.0.0",
    contact={
        "name": "Football Analytics API",
        "email": "support@footballapi.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "type": type(exc).__name__,
        },
    )


# Include routers with API versioning
API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(teams.router, prefix=API_PREFIX)
app.include_router(players.router, prefix=API_PREFIX)
app.include_router(matches.router, prefix=API_PREFIX)
app.include_router(analytics.router, prefix=API_PREFIX)


@app.get("/", tags=["Root"])
def root():
    """API root endpoint with welcome message and navigation links."""
    return {
        "message": "Welcome to the Football Analytics API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": f"{API_PREFIX}/auth",
            "teams": f"{API_PREFIX}/teams",
            "players": f"{API_PREFIX}/players",
            "matches": f"{API_PREFIX}/matches",
            "analytics": f"{API_PREFIX}/analytics",
        },
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "version": "1.0.0"}
