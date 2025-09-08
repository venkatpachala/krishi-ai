# Krishi AI

AI based farmer advisory system in Telugu.

## Development

1. Copy `.env.example` to `.env` and adjust keys.
2. Run `docker compose up --build` to start Postgres, API and web.

## Scripts
- `api/scripts/ingest_pdf.py` – ingest documents to database
- `api/scripts/seed_contacts.py` – seed agriculture officer contacts

## Tests

- Python: `pytest`
- Frontend: `npm test` (placeholder)
