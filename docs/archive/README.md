# Archived Files

Old docs and scripts kept for reference. Use the main docs instead:

- **[README.md](../../README.md)** – Setup, run, test, deploy
- **[PRODUCTION_OPTIMIZATION.md](../../PRODUCTION_OPTIMIZATION.md)** – Deploy, Tailwind, SendGrid, migrations
- **[EMAIL_SETUP.md](../../EMAIL_SETUP.md)** – Gmail SMTP for password reset

## Archived Scripts

| File | Reason |
|------|--------|
| `run_tests.sh` | Use `poetry run pytest tests/ -v` (README) |
| `start.sh` | Use `poetry run python app.py` (README) |
| `encrypt_database.py` | Encryption reverted (see DATABASE_ENCRYPTION_STATUS.md) |
| `migrate_accounts.py` | One-time migration for old DBs |
| `add_categories.py` | One-time script; new users get defaults on signup |

## Archived Docs

| File | Reason |
|------|--------|
| `CHANGES_SUMMARY.txt` | See CHANGELOG.md |
| `DEPLOYMENT_GUIDE.md` | Merged into PRODUCTION_OPTIMIZATION.md |
