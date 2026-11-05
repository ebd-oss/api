from datetime import datetime, timezone

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models import BloodDonation, BloodRequest, BloodRequestResponse, DonorProfile, User


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_donor_profile_blood_group_check(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    session.commit()
    d = DonorProfile(uuid="d1", user_uuid="1", blood_group="INVALID")
    session.add(d)
    with pytest.raises(Exception):
        session.commit()


def test_blood_request_units_positive(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    session.commit()
    r = BloodRequest(uuid="r1", requester_user_uuid="1", blood_group="A+", units_required=0, urgency="normal", contact_name="x", contact_phone="123")
    session.add(r)
    with pytest.raises(Exception):
        session.commit()


def test_blood_request_response_unique(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    d = DonorProfile(uuid="d1", user_uuid="1", blood_group="A+")
    session.add(d)
    r = BloodRequest(uuid="r1", requester_user_uuid="1", blood_group="A+", units_required=1, urgency="normal", contact_name="x", contact_phone="123")
    session.add(r)
    session.commit()
    resp1 = BloodRequestResponse(uuid="resp1", blood_request_uuid="r1", donor_profile_uuid="d1")
    session.add(resp1)
    session.commit()
    resp2 = BloodRequestResponse(uuid="resp2", blood_request_uuid="r1", donor_profile_uuid="d1")
    session.add(resp2)
    with pytest.raises(Exception):
        session.commit()
