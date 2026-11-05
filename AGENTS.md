# Emergency Bangladesh API - Agent Guidelines

## Stack
- Python 3.12+, FastAPI, SQLModel (SQLAlchemy 2), SQLite + SQLCipher
- Pydantic v2 + pydantic-settings, PyJWT, argon2-cffi, PyOTP, Pillow, fastapi-throttle
- Dev: pytest, httpx, ruff, mypy, Alembic (documented deviation)

## Database
- **Sync engine + Session only** (SQLCipher drivers are synchronous, no async DB layer)
- SQLite pragmas: foreign_keys=ON, busy_timeout, journal_mode=WAL
- SQLCipher: PRAGMA key must be first statement on every new connection
- Plain SQLite allowed only for test/development when no key set (logs warning)

## Layout
```
api/
├── app/
│   ├── __init__.py        # exposes FastAPI app
│   ├── config.py, database.py, dependencies.py
│   ├── models/, routes/v1/, services/, schemas/, policies/, lib/
└── tests/
```

## Naming
- Tables plural snake_case, PK is `uuid` on every table
- FKs: `{entity}_uuid` or `{role}_{entity}_uuid`; never `user_id`
- Indexes: `idx_{table}_{column}`, composite `idx_{table}_{col1}_{col2}`
- Python: snake_case functions, PascalCase classes

## API Conventions (for later)
- Prefix `/v1/`, kebab-case endpoints, snake_case JSON/query
- Success: `{data: ...}`, errors: RFC 7807 with string codes + trace_id
- Pagination: offset/limit, routes in `routes/v1/`, logic in `services/`

## Database Rules
- JSON only for audit `previous_values`/`new_values`. Lists are child tables.
- MetaData naming convention enforced in models/base.py
- Every table has `created_at`/`updated_at` via mixin, UTCDateTime rejects naive datetimes
- Enums as StrEnum VARCHAR with named CHECK (native_enum=False)
- Index every FK, location mixin for searchable tables
- FK ondelete RESTRICT by default, CASCADE only for pure child/link rows
- Users never hard-deleted (deleted_at)

## Privacy (Non-negotiable)
- Never store raw NID/passport/birth-registration or government payloads
- Identity docs stored as HMAC-SHA256 keyed with IDENTITY_HASH_PEPPER (never bare hash)
- Public/private/verification data separated
- No medical columns (donor_profiles.blood_group is donor-declared only)

## Commands
- Setup: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt`
- Run: `uvicorn app:app --reload`
- Test: `pytest`
- Lint: `ruff check .`
- Format: `ruff format --check .`
- Type check: `mypy .`
- Migrate: `alembic upgrade head` / `alembic revision --autogenerate -m "..."`

## Git/PR Rules
- Conventional commits (feat:, fix:, chore:, docs:, test:), every commit signed off with `-s`
- Never `--no-verify`, work in branches, PRs only to main
- AI-assisted code must be read and verified by human
- Never commit secrets, .env, *.db, uploads
