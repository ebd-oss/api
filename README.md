# Emergency Bangladesh

**National crisis response, humanitarian coordination, and emergency connectivity platform for Bangladesh.**

Emergency Bangladesh is an open source initiative focused on connecting people, resources, institutions, and emergency services during crises.

> **Right help. Right place. Right time.**

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before contributing.

## License

Licensed under the **Emergency Bangladesh Non-Commercial Research and Study License**.

Commercial use requires explicit written permission from the copyright holder.

## Development setup

1. Create virtual environment: `python -m venv .venv && source .venv/bin/activate`
2. Install dependencies: `pip install -r requirements-dev.txt`
3. Copy environment: `cp .env.example .env` and configure
4. Run migrations: `alembic upgrade head`
5. Start server: `uvicorn app:app --reload`
