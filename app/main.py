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
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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
    redoc_url=None,
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


@app.get("/redoc", include_in_schema=False)
def offline_redoc():
    """
    Offline-friendly API reference page.

    FastAPI's default ReDoc depends on external CDN assets, which can fail in
    restricted networks. This fallback renders the OpenAPI schema directly so
    the documentation remains available locally.
    """
    schema = app.openapi()
    info = schema.get("info", {})
    paths = schema.get("paths", {})
    servers = schema.get("servers", [])
    tag_descriptions = {
        tag.get("name"): tag.get("description", "")
        for tag in schema.get("tags", [])
        if isinstance(tag, dict) and tag.get("name")
    }

    grouped_operations: dict[str, list[dict[str, object]]] = {}
    for path, methods in sorted(paths.items()):
        for method, operation in sorted(methods.items()):
            if method.startswith("x-"):
                continue
            tag = (operation.get("tags") or ["Other"])[0]
            grouped_operations.setdefault(tag, []).append({
                "method": method.upper(),
                "path": path,
                "summary": operation.get("summary") or "No summary provided",
                "description": operation.get("description") or "",
                "parameters": operation.get("parameters") or [],
                "request_body": operation.get("requestBody"),
                "responses": operation.get("responses") or {},
            })

    tag_nav = []
    sections = []
    for tag, operations in grouped_operations.items():
        slug = tag.lower().replace(" ", "-").replace("/", "-")
        tag_nav.append(f'<a href="#{slug}">{tag}</a>')
        tag_description = tag_descriptions.get(tag, "")
        cards = []
        for operation in operations:
            params_html = ""
            if operation["parameters"]:
                param_items = []
                for param in operation["parameters"]:
                    schema_info = param.get("schema", {})
                    schema_type = schema_info.get("type", "object")
                    required = "required" if param.get("required") else "optional"
                    location = param.get("in", "query")
                    description = param.get("description") or "No description"
                    param_items.append(
                        "<li>"
                        f"<strong>{param.get('name')}</strong> "
                        f"<span class='meta'>{location} · {schema_type} · {required}</span>"
                        f"<div>{description}</div>"
                        "</li>"
                    )
                params_html = (
                    "<div class='subsection'><h4>Parameters</h4><ul>"
                    + "".join(param_items)
                    + "</ul></div>"
                )

            request_body = operation["request_body"]
            request_html = ""
            if request_body:
                content = request_body.get("content", {})
                content_types = ", ".join(content.keys()) or "Unknown"
                request_html = (
                    "<div class='subsection'><h4>Request Body</h4>"
                    f"<div class='meta'>{content_types}</div></div>"
                )

            response_items = []
            for status_code, response in operation["responses"].items():
                description = response.get("description") or "No description"
                response_items.append(
                    f"<li><strong>{status_code}</strong> <span>{description}</span></li>"
                )
            responses_html = (
                "<div class='subsection'><h4>Responses</h4><ul>"
                + "".join(response_items)
                + "</ul></div>"
            )

            cards.append(
                "<article class='endpoint'>"
                f"<div class='endpoint-head'><span class='method {operation['method'].lower()}'>{operation['method']}</span>"
                f"<code>{operation['path']}</code></div>"
                f"<h3>{operation['summary']}</h3>"
                + (f"<p>{operation['description']}</p>" if operation["description"] else "")
                + params_html
                + request_html
                + responses_html
                + "</article>"
            )

        sections.append(
            f"<section id='{slug}' class='tag-section'>"
            f"<h2>{tag}</h2>"
            + (f"<p class='tag-description'>{tag_description}</p>" if tag_description else "")
            + "".join(cards)
            + "</section>"
        )

    server_html = ""
    if servers:
        server_items = "".join(f"<li><code>{server.get('url', '')}</code></li>" for server in servers)
        server_html = f"<div class='panel'><h3>Servers</h3><ul>{server_items}</ul></div>"

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>{info.get("title", "API Documentation")} - API Reference</title>
      <style>
        :root {{
          color-scheme: light;
          --bg: #f4f6f8;
          --surface: #ffffff;
          --surface-alt: #eef2f7;
          --text: #1d2733;
          --muted: #5f6b7a;
          --border: #d9e1ea;
          --accent: #0f766e;
          --get: #0f766e;
          --post: #1d4ed8;
          --put: #b45309;
          --delete: #b91c1c;
          --other: #475569;
        }}
        * {{ box-sizing: border-box; }}
        body {{
          margin: 0;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          background: linear-gradient(180deg, #edf2f7 0%, var(--bg) 240px);
          color: var(--text);
        }}
        .hero {{
          padding: 48px 24px 24px;
          background: radial-gradient(circle at top left, #d9f3ef 0, transparent 38%),
                      radial-gradient(circle at top right, #dbeafe 0, transparent 32%);
        }}
        .hero-inner, .content {{
          max-width: 1080px;
          margin: 0 auto;
        }}
        h1, h2, h3, h4 {{ margin: 0 0 12px; }}
        p {{ margin: 0 0 12px; line-height: 1.6; }}
        .subtitle {{ color: var(--muted); max-width: 820px; }}
        .meta-row {{
          display: flex;
          flex-wrap: wrap;
          gap: 12px;
          margin-top: 18px;
        }}
        .panel {{
          background: rgba(255,255,255,0.88);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 16px 18px;
          backdrop-filter: blur(10px);
        }}
        .content {{
          display: grid;
          grid-template-columns: 250px minmax(0, 1fr);
          gap: 24px;
          padding: 24px;
        }}
        .sidebar {{
          position: sticky;
          top: 16px;
          align-self: start;
        }}
        .sidebar nav {{
          display: flex;
          flex-direction: column;
          gap: 8px;
        }}
        .sidebar a {{
          text-decoration: none;
          color: var(--text);
          background: var(--surface);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 10px 12px;
        }}
        .tag-section {{
          margin-bottom: 28px;
        }}
        .tag-description {{
          color: var(--muted);
        }}
        .endpoint {{
          background: var(--surface);
          border: 1px solid var(--border);
          border-radius: 18px;
          padding: 18px;
          margin-top: 14px;
          box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }}
        .endpoint-head {{
          display: flex;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
          margin-bottom: 12px;
        }}
        .method {{
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-width: 72px;
          padding: 6px 10px;
          border-radius: 999px;
          color: white;
          font-size: 0.82rem;
          font-weight: 700;
          letter-spacing: 0.04em;
        }}
        .method.get {{ background: var(--get); }}
        .method.post {{ background: var(--post); }}
        .method.put {{ background: var(--put); }}
        .method.delete {{ background: var(--delete); }}
        .method.patch, .method.options, .method.head {{ background: var(--other); }}
        code {{
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          background: var(--surface-alt);
          padding: 2px 8px;
          border-radius: 8px;
        }}
        .subsection {{
          margin-top: 14px;
          padding-top: 14px;
          border-top: 1px solid var(--border);
        }}
        .subsection ul {{
          margin: 8px 0 0;
          padding-left: 18px;
        }}
        .subsection li {{
          margin-bottom: 8px;
        }}
        .meta {{
          color: var(--muted);
          font-size: 0.92rem;
        }}
        @media (max-width: 900px) {{
          .content {{
            grid-template-columns: 1fr;
          }}
          .sidebar {{
            position: static;
          }}
        }}
      </style>
    </head>
    <body>
      <header class="hero">
        <div class="hero-inner">
          <h1>{info.get("title", "API Documentation")}</h1>
          <p class="subtitle">{info.get("description", "").replace("##", "").replace("**", "")}</p>
          <div class="meta-row">
            <div class="panel"><strong>Version</strong><br>{info.get("version", "N/A")}</div>
            <div class="panel"><strong>OpenAPI Schema</strong><br><a href="/openapi.json">/openapi.json</a></div>
            <div class="panel"><strong>Interactive Docs</strong><br><a href="/docs">/docs</a></div>
            {server_html}
          </div>
        </div>
      </header>
      <main class="content">
        <aside class="sidebar">
          <div class="panel">
            <h3>Sections</h3>
            <nav>{"".join(tag_nav)}</nav>
          </div>
        </aside>
        <div>
          {"".join(sections)}
        </div>
      </main>
    </body>
    </html>
    """
    return HTMLResponse(html)
