# Titanbay Private Markets API

A backend service for managing private market funds, investors, and their investments - built with FastAPI, SQLAlchemy, and PostgreSQL.

## Endpoints

| Method | Path | Description                    |
|---|---|--------------------------------|
| GET | `/funds` | List all funds                 |
| POST | `/funds` | Create a new fund              |
| PUT | `/funds` | Update an existing fund        |
| GET | `/funds/{id}` | Get a specific fund            |
| GET | `/investors` | List all investors             |
| POST | `/investors` | Create a new investor          |
| GET | `/funds/{fund_id}/investments` | List investments for a fund    |
| POST | `/funds/{fund_id}/investments` | Create an investment in a fund |

API endpoint documentation/spec: https://storage.googleapis.com/interview-api-doc-funds.wearebusy.engineering/index.html

## Setup & Run Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL, running locally

### 1. Create the database
Using `psql` or SQL Shell:
```sql
CREATE USER titanbay WITH PASSWORD 'titanbay';
CREATE DATABASE titanbay_funds OWNER titanbay;
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

## Project Structure

## Assumptions & Design Decisions

- **IDs**: UUIDs, generated automatically by the server.
- **`PUT /funds`**: Spec puts `id` in the request body rather than the URL, so this endpoint replaces every field except `id` and `created_at`.
- **Enums**: `Fund.status` (`Fundraising`/`Investing`/`Closed`) and `Investor.investor_type` (`Individual`/`Institution`/`Family Office`) are validated at the API layer via Pydantic in schemas.py
- **`vintage_year`**: Constrained to 1900–2100 as a range - the spec doesn't define bounds, so assumption made here
- **Investor email**: Assumed email must be unique, enforced at database level in models.py; Duplicate returns `409 Conflict`.
- **Investment amount**: Stored as `Numeric`/`Decimal` rather than float, to avoid floating-point rounding errors
- **404s for missing relations**: Creating an investment against a fund or investor ID that doesn't exist returns status code `404` 
- **HTTP status codes**: Followed HTTP status code conventions such as `404` for missing funds/investors, `201` for creating new fund/investor/investment, `409` for conflicting investor emails

## How I Worked With AI Tools

- Used Claude to help with design planning and explaining overall concepts, treating it as an AI assistant rather than writing everything end-to-end. This was so I could fully understand how things come together, and prioritise learning opportunities vs simply getting the task done - e.g. taking time to write things myself followed by seeing what Claude would improve on
- Claude supported in troubleshooting initial environment setup (e.g. Postgres installation and configuration on Windows)
- Challenged Claude where I felt design decisions were more complex than the 2-3 hour scope justified, aiming for a balance between good practice vs something I could explain end-to-end given my current ability and understanding