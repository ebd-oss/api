from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Index
from sqlmodel import Field, SQLModel

from app.models.base import LocationMixin, TimestampMixin, UTCDateTime


class CrisisReport(LocationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "crisis_reports"
    __table_args__ = (
        CheckConstraint(
            "crisis_type IN ('fire','flood','cyclone','earthquake','building_collapse','road_accident','medical_emergency','rescue_requirement','waterlogging','dangerous_infrastructure','missing_person','humanitarian_emergency','other')",
            name="ck_crisis_reports_crisis_type",
        ),
        CheckConstraint(
            "severity IN ('low','moderate','high','critical')",
            name="ck_crisis_reports_severity",
        ),
        CheckConstraint(
            "status IN ('reported','in_verification','services_identified','institutions_notified','response_underway','resolved','archived','rejected')",
            name="ck_crisis_reports_status",
        ),
        CheckConstraint("escalation_level >= 1 AND escalation_level <= 5", name="ck_crisis_reports_escalation_level"),
        CheckConstraint("people_affected >= 0", name="ck_crisis_reports_people_affected"),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    reported_by_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    crisis_type: str = Field(nullable=False)
    severity: str = Field(nullable=False)
    title: str = Field(nullable=False)
    description: str | None = Field(default=None)
    occurred_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    people_affected: int = Field(default=0)
    status: str = Field(default="reported")
    escalation_level: int = Field(default=1)
    verified_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    verified_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")
    resolved_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    archived_at: datetime | None = Field(default=None, sa_type=UTCDateTime)


class CrisisReportNeed(TimestampMixin, SQLModel, table=True):
    __tablename__ = "crisis_report_needs"
    __table_args__ = (
        CheckConstraint(
            "need_type IN ('fire_service','rescue','medical','blood','volunteers','police','shelter','food_water','evacuation','other')",
            name="ck_crisis_report_needs_need_type",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    crisis_report_uuid: str = Field(foreign_key="crisis_reports.uuid", nullable=False)
    need_type: str = Field(nullable=False)
    notes: str | None = Field(default=None)


class CrisisReportMedia(TimestampMixin, SQLModel, table=True):
    __tablename__ = "crisis_report_media"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    crisis_report_uuid: str = Field(foreign_key="crisis_reports.uuid", nullable=False)
    media_file_uuid: str = Field(foreign_key="media_files.uuid", nullable=False)


class CrisisReportStatusHistory(SQLModel, table=True):
    __tablename__ = "crisis_report_status_history"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    crisis_report_uuid: str = Field(foreign_key="crisis_reports.uuid", nullable=False)
    from_status: str | None = Field(default=None)
    to_status: str = Field(nullable=False)
    changed_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")
    note: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=UTCDateTime, nullable=False)


# Indexes
Index("idx_crisis_reports_reported_by_user_uuid", CrisisReport.reported_by_user_uuid)
Index("idx_crisis_reports_verified_by_user_uuid", CrisisReport.verified_by_user_uuid)
Index("idx_crisis_reports_district", CrisisReport.district)
Index("idx_crisis_reports_latitude_longitude", CrisisReport.latitude, CrisisReport.longitude)
Index("idx_crisis_report_needs_crisis_report_uuid", CrisisReportNeed.crisis_report_uuid)
Index("idx_crisis_report_media_crisis_report_uuid", CrisisReportMedia.crisis_report_uuid)
Index("idx_crisis_report_media_media_file_uuid", CrisisReportMedia.media_file_uuid)
Index("idx_crisis_report_status_history_crisis_report_uuid", CrisisReportStatusHistory.crisis_report_uuid)
Index("idx_crisis_report_status_history_changed_by_user_uuid", CrisisReportStatusHistory.changed_by_user_uuid)
Index("uq_crisis_report_needs_report_need", CrisisReportNeed.crisis_report_uuid, CrisisReportNeed.need_type, unique=True)
