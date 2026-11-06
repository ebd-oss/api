# Emergency Bangladesh API - Agent Guidelines

## Stack

Language: Python 3.13+  
Libraries: fastapi[all], sqlmodel, sqlcipher3-binary, pydantic[email], pydantic-settings, pyjwt, argon2-cffi, pyotp, pillow

## Naming (as Per ADRs)

- Tables plural snake_case, PK is `uuid` of UUID type on every table.
- FKs: `{entity}_uuid`. Example: `volunteer_uuid`, `account_uuid` etc.
- Indexes (Only if handled manually): `idx_{table}_{column}`, composite `idx_{table}_{col1}_{col2}`
- Python: snake_case functions & variables, PascalCase classes

## API Conventions (for later)

- Prefix `/v1/`, kebab-case endpoints, snake_case JSON/query
- Success: `{data: ...}`, errors: RFC 7807 with string codes + trace_id
- Pagination: offset/limit

## Database Rules

- JSON only for audit `previous_values`/`new_values`. Lists are child tables.
- MetaData naming convention enforced in models/base.py
- Every table has `created_at`/`updated_at` via mixin, UTCDateTime rejects naive datetimes
- Enums as StrEnum VARCHAR with named CHECK (native_enum=False)
- Index every FK, location mixin for searchable tables
- Accounts are never hard-deleted (Turn deleted=True, keep all data for audit)

## Privacy (Non-negotiable)

- Never store raw NID/passport/birth-registration or government payloads
- Identity docs stored as HMAC-SHA256 keyed with IDENTITY_HASH_PEPPER (never bare hash)
- Public/private/verification data separated
- No medical columns (donor_profiles.blood_group is donor-declared only)

## Commit Rules

- Conventional commits (feat:, fix:, chore:, docs:, test:), every commit adds `-s` and `-S` flags.
- No push to origin/main. Create a new branch for every piece of work.
- Record sensitive ones in .gitignore before committing.
