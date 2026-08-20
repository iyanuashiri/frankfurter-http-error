# Currency Converter Project

## Description

This project is a FastAPI-based currency converter that uses the Frankfurter API to fetch exchange rates and supports user management, conversions, and history tracking.

## Technologies

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn
- SQLite (default)
- Frankfurter API

## Prerequisites

- Python 3.12 or newer
- uv installed
- Docker installed (for containerized run)

## Project structure

- app/: FastAPI application code
- alembic/: database migrations
- tests/: pytest test suite
- .env: environment variables for local development
- Dockerfile: container configuration

## Local development with uv

From the backend directory:

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

Then open:

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

## Docker

From the project root:

```bash
docker build -f backend/Dockerfile -t harbor-currency-converter-project backend
docker run -p 8000:8000 harbor-currency-converter-project
```

The container automatically runs the database migrations before starting the app, so the SQLite database is initialized for you.

## Environment variables

The app reads configuration from a local `.env` file in the backend directory. Example:

```env
DATABASE_URL=sqlite:///./currency.db
FRANKFURTER_HOST=api.frankfurter.dev
```

## Authentication

The API uses an API key for authentication. The key is passed in the `X-API-Key` header and is generated when a user is created.

## Rate Limiting

The API enforces a rate limit of 10 requests per minute per user. If exceeded, the API returns HTTP 429.

## Credits

Each user starts with 10 credits. Each request costs 1 credit. Once credits are exhausted, the API returns HTTP 403.

## Usage

1. Create a user with a username and password at `/api/v1/users/`.
2. Get available currencies at `/api/v1/currencies/`.
3. Create a conversion at `/api/v1/conversions/`.
4. View historical rates at `/api/v1/historical-rates/{date}`.
5. View conversion history at `/api/v1/history/`.
6. List users at `/api/v1/users/`.

## Example requests

```bash
# Create a user
POST http://localhost:8000/api/v1/users/
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpassword"
}

# Get currencies
GET http://localhost:8000/api/v1/currencies/

# Get conversion rates
POST http://localhost:8000/api/v1/conversions/
Content-Type: application/json

{
  "base_currency": "USD",
  "target_currency": "EUR",
  "amount": 100
}

# Get historical currency rates
GET http://localhost:8000/api/v1/historical-rates/2023-01-01

# Get history for the current user
GET http://localhost:8000/api/v1/history/
```

## API Documentation

Open the interactive API docs at:

```text
http://localhost:8000/docs
```

## Testing

Run the test suite with:

```bash
cd backend
uv run pytest -v
```

You can also run a subset of tests if needed.

## License

MIT