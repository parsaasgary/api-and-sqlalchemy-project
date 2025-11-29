# Football Fantasy League API

A FastAPI-based REST API for managing and querying data from a football fantasy league. This project demonstrates the use of FastAPI, SQLAlchemy, and Docker to create a production-ready API for fantasy football data analytics.

## Overview

This API provides endpoints to access information about:
- **Players**: NFL players in the fantasy league
- **Teams**: Fantasy football teams and their rosters
- **Leagues**: SWC fantasy football leagues
- **Performances**: Weekly player performances with fantasy points
- **Analytics**: Health checks and data counts

## Features

- RESTful API with FastAPI
- SQLAlchemy ORM for database operations
- Pydantic models for data validation
- Interactive API documentation (Swagger UI)
- Docker containerization support
- Comprehensive query filtering and pagination
- Health check endpoints

## Project Structure

```
.
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── schemas.py           # Pydantic models for request/response validation
│   └── test_main.py         # API tests
├── Database/
│   ├── __init__.py
│   ├── create_db_and_tabels.py  # Database schema creation
│   ├── CRUD.py              # Database operations
│   ├── load-data-to-db.py   # Data loading scripts
│   ├── test_CRUD.py         # CRUD tests
│   ├── fantasy_data.db      # SQLite database
│   └── data/                # CSV data files
│       ├── league_data.csv
│       ├── performance_data.csv
│       ├── player_data.csv
│       ├── team_data.csv
│       └── team_player_data.csv
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI
- **Python 3.12**: Programming language
- **Docker**: Containerization platform

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Installation

### Local Development Setup

1. **Clone the repository** (or navigate to the project directory):
   ```bash
   cd "api for datascience book"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ensure the database is set up**:
   The project includes a SQLite database (`Database/fantasy_data.db`). If you need to recreate it:
   ```bash
   python Database/create_db_and_tabels.py
   python Database/load-data-to-db.py
   ```

## Running the Application

### Local Development

Run the FastAPI application using uvicorn:

```bash
uvicorn api.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t football-fantasy-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 football-fantasy-api
   ```

The API will be accessible at http://localhost:8000

## API Endpoints

### Analytics

- **GET /** - Health check endpoint
  - Returns: `{"massage": "API works fine"}`

- **GET /v0/counts/** - Get counts of leagues, teams, and players
  - Returns: Count statistics for the database

### Players

- **GET /v0/players/** - Get list of players
  - Query Parameters:
    - `skip` (int, default: 0): Pagination offset
    - `limit` (int, default: 100): Number of records to return
    - `min_last_changed_date` (date, optional): Filter by last changed date
    - `player_first_name` (str, optional): Filter by first name
    - `player_last_name` (str, optional): Filter by last name

- **GET /v0/player/{player_id}** - Get a specific player by ID
  - Path Parameters:
    - `player_id` (int): Player ID

### Scoring

- **GET /v0/performance/** - Get list of player performances
  - Query Parameters:
    - `min_last_date_changed` (date, default: 0): Filter by date
    - `skip` (int, default: 0): Pagination offset
    - `limit` (int, default: 100): Number of records to return

### Membership

- **GET /v0/leagues/** - Get list of leagues
  - Query Parameters:
    - `min_last_date_changed` (date, optional): Filter by date
    - `skip` (int, default: 0): Pagination offset
    - `limit` (int, default: 100): Number of records to return
    - `league_name` (str, optional): Filter by league name

- **GET /v0/league/{league_id}** - Get a specific league by ID
  - Path Parameters:
    - `league_id` (int): League ID

- **GET /v0/teams/** - Get list of teams
  - Query Parameters:
    - `skip` (int, default: 0): Pagination offset
    - `limit` (int, default: 100): Number of records to return
    - `minimum_last_changed_date` (date, optional): Filter by date
    - `team_name` (str, optional): Filter by team name
    - `league_id` (int, optional): Filter by league ID

## Example API Calls

### Health Check
```bash
curl http://localhost:8000/
```

### Get Players
```bash
curl "http://localhost:8000/v0/players/?skip=0&limit=10"
```

### Get Player by ID
```bash
curl http://localhost:8000/v0/player/1
```

### Get Counts
```bash
curl http://localhost:8000/v0/counts/
```

## Testing

Run the test suite:

```bash
pytest api/test_main.py
pytest Database/test_CRUD.py
```

## Development Notes

- The API uses SQLAlchemy for database operations
- Database sessions are managed through FastAPI dependencies
- All endpoints support pagination via `skip` and `limit` parameters
- The database is SQLite, located at `Database/fantasy_data.db`
- The project structure separates concerns: API routes, database operations, and data models

## License

This is a learning project for practicing FastAPI and SQLAlchemy.

## Version

Current version: **0.1**

