# LaudatorAI Backend

AI-Powered Job Application Assistant Backend API.

## Features

- FastAPI-based REST API
- Job description extraction from URLs
- Resume parsing and tailoring
- Cover letter generation
- File storage with MinIO
- Background task processing with Celery

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis
- MinIO (optional, for file storage)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration.

### Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Development

### Code Formatting

```bash
# Format code
black app/

# Sort imports
isort app/

# Type checking
mypy app/
```

### Running Tests

```bash
pytest
```

## Project Structure

```
app/
├── api/                    # API endpoints
│   └── v1/
│       ├── api.py         # Main API router
│       └── endpoints/     # Individual endpoint modules
├── core/                  # Core application modules
│   └── config.py         # Configuration settings
├── models/               # Database models
├── schemas/              # Pydantic schemas
├── services/             # Business logic
├── utils/                # Utility functions
└── main.py              # Application entry point
```
