from datetime import datetime, timezone

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models import CrisisReport, CrisisReportNeed, User


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_crisis_escalation_level_check(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    session.commit()
    c = CrisisReport(uuid="c1", reported_by_user_uuid="1", crisis_type="fire", severity="high", title="x", escalation_level=6)
    session.add(c)
    with pytest.raises(Exception):
        session.commit()


def test_crisis_need_unique(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    c = CrisisReport(uuid="c1", reported_by_user_uuid="1", crisis_type="fire", severity="high", title="x")
    session.add(c)
    session.commit()
    n1 = CrisisReportNeed(uuid="n1", crisis_report_uuid="c1", need_type="fire_service")
    session.add(n1)
    session.commit()
    n2 = CrisisReportNeed(uuid="n2", crisis_report_uuid="c1", need_type="fire_service")
    session.add(n2)
    with pytest.raises(Exception):
        session.commit()
