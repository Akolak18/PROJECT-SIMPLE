# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
cp .env.example .env          # Fill in credentials (see below)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py                  # Serves at http://localhost:5000
```

Required `.env` variables:
- `PREVIO_USERNAME` / `PREVIO_PASSWORD` — Previo PMS login credentials
- `PREVIO_HOTEL_ID` — Hotel ID in the Previo system
- `FLASK_SECRET_KEY` — Flask session key
- `REFRESH_INTERVAL` — Frontend polling interval in seconds (default 60)
- `FLASK_PORT` — Optional, defaults to 5000

There are no tests or linter configurations in this project.

## Architecture

This is a single-purpose Flask web app that pulls hotel room reservations from the Previo PMS API and presents them to cleaning staff as a real-time table and downloadable Excel file.

**Data flow:**

```
templates/index.html   (vanilla JS SPA, polls /api/reservations every N seconds)
        ↓ HTTP (date range params)
app.py routes          (/, /api/reservations, /export/excel)
        ↓ delegates to
previo_client.py       (Previo REST API via Basic Auth → flattens + normalizes rows)
        ↓ rows
excel_export.py        (converts rows to styled .xlsx workbook for download)
```

**Three backend modules:**

- `previo_client.py` — All Previo PMS integration. Handles authentication, defensive multi-version API response parsing, flattening multi-room bookings into individual rows, field normalization, and status code mapping. This is the most complex module.
- `excel_export.py` — Converts normalized row dicts into a formatted `.xlsx` workbook (color-coded rows: green = arriving today, orange = departing/needs cleaning).
- `app.py` — Flask routes only. Reads date range from request params, calls the client, and delegates to excel_export for downloads. No business logic lives here.

**Frontend (`templates/index.html`):**  
A single Jinja2 template rendered with `date_from`, `date_to`, and `refresh_interval` variables. Vanilla JS polls `/api/reservations`, renders the table, and applies the same color-coding logic as the Excel export. No JS framework or bundler.

## Key conventions

- `previo_client.py` uses defensive parsing throughout because the Previo API returns different shapes across versions — always check both possible field paths when adding new fields.
- Color-coding semantics are shared between the frontend JS and `excel_export.py`; keep them in sync when changing status logic.
- The app is stateless — no database, no session data. Every request re-fetches from Previo.
- `app.run(debug=True)` is set in `app.py`; change to `debug=False` before deploying to production.
