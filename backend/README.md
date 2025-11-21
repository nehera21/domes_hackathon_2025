# Backend

FastAPI backend for the hackathon project.

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Make sure `.env` file exists (it should be created automatically)

3. Run the server:
```bash
uv run python -m backend.main
```

4. Visit the API docs at http://localhost:8000/docs

## Structure

- `main.py` - Application entry point and route registration
- `settings.py` - Configuration loaded from environment variables
- `databridge.py` - Database connection layer
- `models/` - Pydantic models for validation and serialization
- `services/` - Business logic layer
- `routers/` - API route handlers

## Development

The server runs with auto-reload in debug mode. Changes to Python files will automatically restart the server.

### Code Quality

```bash
uv run black .        # Format code
uv run ruff check .   # Lint code
```

