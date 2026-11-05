from datetime import datetime, timezone

import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.models import Mission, User, VolunteerProfile, VolunteerSkill, Skill


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


def test_mission_volunteers_needed_positive(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    session.commit()
    m = Mission(uuid="m1", created_by_user_uuid="1", title="x", volunteers_needed=0)
    session.add(m)
    with pytest.raises(Exception):
        session.commit()


def test_volunteer_skill_unique(session):
    u = User(uuid="1", account_type="individual", status="active", email="a@b.com")
    session.add(u)
    vp = VolunteerProfile(uuid="vp1", user_uuid="1")
    s = Skill(uuid="s1", name="first_aid", category="medical")
    session.add(vp)
    session.add(s)
    session.commit()
    vs1 = VolunteerSkill(uuid="vs1", volunteer_profile_uuid="vp1", skill_uuid="s1")
    session.add(vs1)
    session.commit()
    vs2 = VolunteerSkill(uuid="vs2", volunteer_profile_uuid="vp1", skill_uuid="s1")
    session.add(vs2)
    with pytest.raises(Exception):
        session.commit()
