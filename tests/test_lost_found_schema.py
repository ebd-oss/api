from datetime import datetime, timezone

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models import LostFoundMatch, LostFoundReport, MissingPersonCase, User


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_missing_person_public_requires_verified(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    r = LostFoundReport(uuid="r1", reported_by_user_uuid="1", report_type="missing_person", title="x", contact_preference="phone")
    session.add(r)
    session.commit()
    m = MissingPersonCase(uuid="m1", lost_found_report_uuid="r1", person_name="x", verification_status="pending", is_public=True)
    session.add(m)
    with pytest.raises(Exception):
        session.commit()


def test_lost_found_match_different(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    r1 = LostFoundReport(uuid="r1", reported_by_user_uuid="1", report_type="lost_item", title="x", contact_preference="phone")
    r2 = LostFoundReport(uuid="r2", reported_by_user_uuid="1", report_type="found_item", title="y", contact_preference="phone")
    session.add(r1)
    session.add(r2)
    session.commit()
    m = LostFoundMatch(uuid="m1", lost_report_uuid="r1", found_report_uuid="r1")
    session.add(m)
    with pytest.raises(Exception):
        session.commit()
