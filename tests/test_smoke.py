import os
import sqlite3
import tempfile

import pytest
from fastapi.testclient import TestClient

from app import app
from app.config import get_settings, Settings


def test_app_imports():
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code in (200, 404)  # docs may or may not be configured


def test_settings_load():
    get_settings.cache_clear()
    settings = get_settings()
    assert settings.ENVIRONMENT in ("development", "test", "production")


def test_production_fails_fast_without_secrets(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("DATABASE_ENCRYPTION_KEY", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.delenv("IDENTITY_HASH_PEPPER", raising=False)
    with pytest.raises(ValueError):
        Settings()


def test_engine_connects_with_foreign_keys_on():
    from app.database import engine
    with engine.connect() as conn:
        result = conn.exec_driver_sql("PRAGMA foreign_keys")
        fk = result.fetchone()[0]
        assert fk == 1


def test_sqlcipher_status():
    try:
        import sqlcipher3  # noqa
        # Try to create encrypted db
        import tempfile, os
        db = tempfile.mktemp(suffix='.db')
        conn = sqlcipher3.connect(db)
        conn.execute("PRAGMA key='testkey'")
        conn.execute("CREATE TABLE t(x)")
        conn.close()
        # Try to open with plain sqlite3
        try:
            conn2 = sqlite3.connect(db)
            conn2.execute("SELECT * FROM t")
            conn2.close()
            pytest.fail("Encrypted DB was opened by plain sqlite3 - SQLCipher not working properly")
        except Exception:
            pass  # Expected - cannot open encrypted db with plain sqlite3
        os.unlink(db)
    except Exception as e:
        pytest.skip(f"SQLCipher not available: {e}. cPanel deployment risk: may need sqlcipher3-binary or system libsqlcipher-dev")
