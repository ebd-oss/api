from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Index
from sqlmodel import Field, SQLModel

from app.models.base import LocationMixin, TimestampMixin, UTCDateTime


class VolunteerProfile(LocationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_profiles"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','inactive','suspended')",
            name="ck_volunteer_profiles_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False, unique=True)
    status: str = Field(default="active")
    is_available: bool = Field(default=True)
    availability_notes: str | None = Field(default=None)
    experience_summary: str | None = Field(default=None)
    years_of_experience: int | None = Field(default=None)
    verified_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    verified_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")


class Skill(TimestampMixin, SQLModel, table=True):
    __tablename__ = "skills"
    __table_args__ = (
        CheckConstraint(
            "category IN ('medical','rescue','logistics','communication','technical','other')",
            name="ck_skills_category",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(nullable=False, unique=True)
    category: str = Field(nullable=False)
    description: str | None = Field(default=None)


class VolunteerSkill(TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_skills"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    volunteer_profile_uuid: str = Field(foreign_key="volunteer_profiles.uuid", nullable=False)
    skill_uuid: str = Field(foreign_key="skills.uuid", nullable=False)


class VolunteerLanguage(TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_languages"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    volunteer_profile_uuid: str = Field(foreign_key="volunteer_profiles.uuid", nullable=False)
    language_code: str = Field(nullable=False)
    proficiency: str | None = Field(default=None)


class VolunteerCertification(TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_certifications"
    __table_args__ = (
        CheckConstraint(
            "verification_status IN ('pending','verified','rejected')",
            name="ck_volunteer_certifications_verification_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    volunteer_profile_uuid: str = Field(foreign_key="volunteer_profiles.uuid", nullable=False)
    name: str = Field(nullable=False)
    issuer: str | None = Field(default=None)
    issued_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    expires_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    verification_status: str = Field(default="pending")


class VolunteerTransportMode(TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_transport_modes"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    volunteer_profile_uuid: str = Field(foreign_key="volunteer_profiles.uuid", nullable=False)
    mode: str = Field(nullable=False)


class VolunteerTeam(LocationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_teams"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active','inactive','disbanded')",
            name="ck_volunteer_teams_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    leader_volunteer_profile_uuid: str = Field(foreign_key="volunteer_profiles.uuid", nullable=False)
    status: str = Field(default="active")


class VolunteerTeamMember(TimestampMixin, SQLModel, table=True):
    __tablename__ = "volunteer_team_members"
    __table_args__ = (
        CheckConstraint(
            "role IN ('leader','member')",
            name="ck_volunteer_team_members_role",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    volunteer_team_uuid: str = Field(foreign_key="volunteer_teams.uuid", nullable=False)
    volunteer_profile_uuid: str = Field(foreign_key="volunteer_profiles.uuid", nullable=False)
    role: str = Field(default="member")
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=UTCDateTime, nullable=False)
    left_at: datetime | None = Field(default=None, sa_type=UTCDateTime)


class Mission(LocationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "missions"
    __table_args__ = (
        CheckConstraint("volunteers_needed > 0", name="ck_missions_volunteers_needed_positive"),
        CheckConstraint(
            "status IN ('need_identified','mission_created','team_assigned','team_travelling','team_arrived','work_underway','mission_completed','cancelled')",
            name="ck_missions_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_by_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    crisis_report_uuid: str | None = Field(default=None, foreign_key="crisis_reports.uuid")
    title: str = Field(nullable=False)
    description: str | None = Field(default=None)
    volunteers_needed: int = Field(nullable=False)
    priority: str | None = Field(default=None)
    status: str = Field(default="need_identified")
    started_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    completed_at: datetime | None = Field(default=None, sa_type=UTCDateTime)


class MissionTeamAssignment(TimestampMixin, SQLModel, table=True):
    __tablename__ = "mission_team_assignments"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    mission_uuid: str = Field(foreign_key="missions.uuid", nullable=False)
    volunteer_team_uuid: str = Field(foreign_key="volunteer_teams.uuid", nullable=False)
    assigned_by_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=UTCDateTime, nullable=False)
    unassigned_at: datetime | None = Field(default=None, sa_type=UTCDateTime)


class MissionStatusHistory(SQLModel, table=True):
    __tablename__ = "mission_status_history"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    mission_uuid: str = Field(foreign_key="missions.uuid", nullable=False)
    from_status: str | None = Field(default=None)
    to_status: str = Field(nullable=False)
    changed_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")
    note: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=UTCDateTime, nullable=False)


# Indexes
Index("idx_volunteer_profiles_user_uuid", VolunteerProfile.user_uuid)
Index("idx_volunteer_profiles_verified_by_user_uuid", VolunteerProfile.verified_by_user_uuid)
Index("idx_volunteer_profiles_district", VolunteerProfile.district)
Index("idx_volunteer_profiles_latitude_longitude", VolunteerProfile.latitude, VolunteerProfile.longitude)
Index("idx_volunteer_skills_volunteer_profile_uuid", VolunteerSkill.volunteer_profile_uuid)
Index("idx_volunteer_skills_skill_uuid", VolunteerSkill.skill_uuid)
Index("idx_volunteer_languages_volunteer_profile_uuid", VolunteerLanguage.volunteer_profile_uuid)
Index("idx_volunteer_certifications_volunteer_profile_uuid", VolunteerCertification.volunteer_profile_uuid)
Index("idx_volunteer_transport_modes_volunteer_profile_uuid", VolunteerTransportMode.volunteer_profile_uuid)
Index("idx_volunteer_teams_leader_volunteer_profile_uuid", VolunteerTeam.leader_volunteer_profile_uuid)
Index("idx_volunteer_teams_district", VolunteerTeam.district)
Index("idx_volunteer_teams_latitude_longitude", VolunteerTeam.latitude, VolunteerTeam.longitude)
Index("idx_volunteer_team_members_volunteer_team_uuid", VolunteerTeamMember.volunteer_team_uuid)
Index("idx_volunteer_team_members_volunteer_profile_uuid", VolunteerTeamMember.volunteer_profile_uuid)
Index("idx_missions_created_by_user_uuid", Mission.created_by_user_uuid)
Index("idx_missions_crisis_report_uuid", Mission.crisis_report_uuid)
Index("idx_missions_district", Mission.district)
Index("idx_missions_latitude_longitude", Mission.latitude, Mission.longitude)
Index("idx_mission_team_assignments_mission_uuid", MissionTeamAssignment.mission_uuid)
Index("idx_mission_team_assignments_volunteer_team_uuid", MissionTeamAssignment.volunteer_team_uuid)
Index("idx_mission_team_assignments_assigned_by_user_uuid", MissionTeamAssignment.assigned_by_user_uuid)
Index("idx_mission_status_history_mission_uuid", MissionStatusHistory.mission_uuid)
Index("idx_mission_status_history_changed_by_user_uuid", MissionStatusHistory.changed_by_user_uuid)
Index("uq_volunteer_skills_profile_skill", VolunteerSkill.volunteer_profile_uuid, VolunteerSkill.skill_uuid, unique=True)
Index("uq_volunteer_languages_profile_lang", VolunteerLanguage.volunteer_profile_uuid, VolunteerLanguage.language_code, unique=True)
Index("uq_volunteer_transport_modes_profile_mode", VolunteerTransportMode.volunteer_profile_uuid, VolunteerTransportMode.mode, unique=True)
Index("uq_volunteer_team_members_team_profile", VolunteerTeamMember.volunteer_team_uuid, VolunteerTeamMember.volunteer_profile_uuid, unique=True)
