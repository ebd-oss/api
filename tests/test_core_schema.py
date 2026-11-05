import sqlite3
from datetime import datetime, timezone

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models import (
    AuditLog,
    IdentityVerification,
    MediaFile,
    OtpChallenge,
    Permission,
    PermissionGroup,
    PermissionGroupPermission,
    RefreshToken,
    User,
    UserPermissionGrant,
    UserPrivateDetail,
    UserProfile,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    # Add triggers
    with engine.connect() as conn:
        conn.exec_driver_sql("""
            CREATE TRIGGER IF NOT EXISTS audit_logs_no_update
            BEFORE UPDATE ON audit_logs
            BEGIN
                SELECT RAISE(ABORT, 'audit_logs are append-only');
            END;
        """)
        conn.exec_driver_sql("""
            CREATE TRIGGER IF NOT EXISTS audit_logs_no_delete
            BEFORE DELETE ON audit_logs
            BEGIN
                SELECT RAISE(ABORT, 'audit_logs are append-only');
            END;
        """)
        conn.commit()
    with Session(engine) as s:
        yield s


def test_user_email_or_phone_check(session):
    with pytest.raises(Exception):
        u = User(uuid="1", account_type="individual", status="active")
        session.add(u)
        session.commit()


def test_user_unique_email_phone(session):
    u1 = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u1)
    session.commit()
    u2 = User(uuid="2", account_type="individual", status="active", email="a@b.com")
    session.add(u2)
    with pytest.raises(Exception):
        session.commit()


def test_audit_log_append_only(session):
    log = AuditLog(uuid="1", action="test", entity_type="user", entity_uuid="x", created_at=datetime.now(timezone.utc))
    session.add(log)
    session.commit()
    log.action = "changed"
    session.add(log)
    with pytest.raises(Exception):
        session.commit()
    session.rollback()
    with pytest.raises(Exception):
        session.execute(__import__('sqlalchemy').text("DELETE FROM audit_logs"))
        session.commit()


def test_identity_verification_partial_unique(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    session.commit()
    iv1 = IdentityVerification(uuid="1", user_uuid="1", method="national_id", status="verified", document_hash="hash1", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    session.add(iv1)
    session.commit()
    iv2 = IdentityVerification(uuid="2", user_uuid="1", method="national_id", status="verified", document_hash="hash1", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    session.add(iv2)
    with pytest.raises(Exception):
        session.commit()


def test_pbac_exactly_one(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    p = Permission(uuid="p1", code="test.view", resource="test", action="view", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    session.add(p)
    session.commit()
    g = UserPermissionGrant(uuid="g1", user_uuid="1", permission_uuid="p1", permission_group_uuid="g1", granted_by_user_uuid="1", purpose="test", created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
    session.add(g)
    with pytest.raises(Exception):
        session.commit()
