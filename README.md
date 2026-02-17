# Harit Finance

Personal finance app – track expenses, income, accounts, and transfers.

## Quick Start

```bash
poetry install && poetry run python app.py
```

Open **http://localhost:5001**

## Setup & Run

| Step | Command |
|------|---------|
| Install | `poetry install` |
| Run | `poetry run python app.py` |
| Test | `poetry run pytest tests/ -v` |

Optional: `cp .env.example .env` and add `MAIL_*` vars for password reset.

## Testing

```bash
# Run all tests
poetry run pytest tests/ -v

# Run specific test file
poetry run pytest tests/test_security.py -v

# Run with less output
poetry run pytest tests/ -q
```

## Deploy (Render)

1. Push to GitHub → Connect repo in Render
2. Add env vars: `SECRET_KEY`, `DATABASE_URL`, `MAIL_*`
3. Deploy

## Docs

| Doc | Purpose |
|-----|---------|
| [PRODUCTION_OPTIMIZATION.md](PRODUCTION_OPTIMIZATION.md) | Deploy, Tailwind, SendGrid, migrations |
| [EMAIL_SETUP.md](EMAIL_SETUP.md) | Gmail SMTP for password reset |
