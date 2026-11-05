from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Index
from sqlmodel import Field, SQLModel

from app.models.base import LocationMixin, ModerationMixin, TimestampMixin, UTCDateTime


class LostFoundReport(LocationMixin, ModerationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "lost_found_reports"
    __table_args__ = (
        CheckConstraint(
            "report_type IN ('lost_item','found_item','missing_person')",
            name="ck_lost_found_reports_report_type",
        ),
        CheckConstraint(
            "contact_preference IN ('in_app','phone','email')",
            name="ck_lost_found_reports_contact_preference",
        ),
        CheckConstraint(
            "status IN ('open','matched','resolved','closed')",
            name="ck_lost_found_reports_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    reported_by_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    report_type: str = Field(nullable=False)
    category: str | None = Field(default=None)
    title: str = Field(nullable=False)
    description: str | None = Field(default=None)
    identifying_information: str | None = Field(default=None)
    occurred_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    contact_preference: str = Field(nullable=False)
    status: str = Field(default="open")


class MissingPersonCase(TimestampMixin, SQLModel, table=True):
    __tablename__ = "missing_person_cases"
    __table_args__ = (
        CheckConstraint(
            "(is_public = 0) OR (is_public = 1 AND verification_status = 'verified')",
            name="ck_missing_person_cases_public_verified",
        ),
        CheckConstraint(
            "verification_status IN ('pending','verified','rejected')",
            name="ck_missing_person_cases_verification_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    lost_found_report_uuid: str = Field(foreign_key="lost_found_reports.uuid", nullable=False, unique=True)
    person_name: str = Field(nullable=False)
    age_years: int | None = Field(default=None)
    gender: str | None = Field(default=None)
    is_minor: bool = Field(default=False)
    physical_description: str | None = Field(default=None)
    last_seen_clothing: str | None = Field(default=None)
    guardian_contact_phone: str | None = Field(default=None)
    police_report_reference: str | None = Field(default=None)
    verification_status: str = Field(default="pending")
    verified_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")
    verified_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    is_public: bool = Field(default=False)


class LostFoundReportMedia(TimestampMixin, SQLModel, table=True):
    __tablename__ = "lost_found_report_media"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    lost_found_report_uuid: str = Field(foreign_key="lost_found_reports.uuid", nullable=False)
    media_file_uuid: str = Field(foreign_key="media_files.uuid", nullable=False)


class LostFoundMatch(TimestampMixin, SQLModel, table=True):
    __tablename__ = "lost_found_matches"
    __table_args__ = (
        CheckConstraint("lost_report_uuid != found_report_uuid", name="ck_lost_found_matches_different"),
        CheckConstraint(
            "status IN ('suggested','confirmed','dismissed')",
            name="ck_lost_found_matches_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    lost_report_uuid: str = Field(foreign_key="lost_found_reports.uuid", nullable=False)
    found_report_uuid: str = Field(foreign_key="lost_found_reports.uuid", nullable=False)
    status: str = Field(default="suggested")
    score: float | None = Field(default=None)
    confirmed_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")


# Indexes
Index("idx_lost_found_reports_reported_by_user_uuid", LostFoundReport.reported_by_user_uuid)
Index("idx_lost_found_reports_district", LostFoundReport.district)
Index("idx_lost_found_reports_latitude_longitude", LostFoundReport.latitude, LostFoundReport.longitude)
Index("idx_missing_person_cases_lost_found_report_uuid", MissingPersonCase.lost_found_report_uuid)
Index("idx_missing_person_cases_verified_by_user_uuid", MissingPersonCase.verified_by_user_uuid)
Index("idx_lost_found_report_media_lost_found_report_uuid", LostFoundReportMedia.lost_found_report_uuid)
Index("idx_lost_found_report_media_media_file_uuid", LostFoundReportMedia.media_file_uuid)
Index("idx_lost_found_matches_lost_report_uuid", LostFoundMatch.lost_report_uuid)
Index("idx_lost_found_matches_found_report_uuid", LostFoundMatch.found_report_uuid)
Index("idx_lost_found_matches_confirmed_by_user_uuid", LostFoundMatch.confirmed_by_user_uuid)
Index("uq_lost_found_matches_pair", LostFoundMatch.lost_report_uuid, LostFoundMatch.found_report_uuid, unique=True)
