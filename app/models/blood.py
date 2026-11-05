from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint, Index
from sqlmodel import Field, SQLModel

from app.models.base import LocationMixin, ModerationMixin, TimestampMixin, UTCDateTime


class DonorProfile(LocationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "donor_profiles"
    __table_args__ = (
        CheckConstraint(
            "blood_group IN ('A+','A-','B+','B-','AB+','AB-','O+','O-')",
            name="ck_donor_profiles_blood_group",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False, unique=True)
    blood_group: str = Field(nullable=False)
    is_available: bool = Field(default=True)
    last_donated_at: datetime | None = Field(default=None, sa_type=UTCDateTime)


class BloodRequest(LocationMixin, ModerationMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "blood_requests"
    __table_args__ = (
        CheckConstraint("units_required > 0", name="ck_blood_requests_units_required_positive"),
        CheckConstraint("units_fulfilled >= 0 AND units_fulfilled <= units_required", name="ck_blood_requests_units_fulfilled_range"),
        CheckConstraint(
            "blood_group IN ('A+','A-','B+','B-','AB+','AB-','O+','O-')",
            name="ck_blood_requests_blood_group",
        ),
        CheckConstraint(
            "urgency IN ('critical','urgent','normal')",
            name="ck_blood_requests_urgency",
        ),
        CheckConstraint(
            "status IN ('open','partially_fulfilled','fulfilled','cancelled','expired')",
            name="ck_blood_requests_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    requester_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    blood_group: str = Field(nullable=False)
    blood_component: str = Field(default="whole_blood")
    units_required: int = Field(nullable=False)
    units_fulfilled: int = Field(default=0)
    hospital_name: str | None = Field(default=None)
    required_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    urgency: str = Field(nullable=False)
    contact_name: str = Field(nullable=False)
    contact_phone: str = Field(nullable=False)
    details: str | None = Field(default=None)
    status: str = Field(default="open")


class BloodRequestResponse(TimestampMixin, SQLModel, table=True):
    __tablename__ = "blood_request_responses"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','accepted','declined','withdrawn','donated')",
            name="ck_blood_request_responses_status",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    blood_request_uuid: str = Field(foreign_key="blood_requests.uuid", nullable=False)
    donor_profile_uuid: str = Field(foreign_key="donor_profiles.uuid", nullable=False)
    status: str = Field(default="pending")
    message: str | None = Field(default=None)
    responded_at: datetime | None = Field(default=None, sa_type=UTCDateTime)


class BloodDonation(TimestampMixin, SQLModel, table=True):
    __tablename__ = "blood_donations"
    __table_args__ = (
        CheckConstraint("units > 0", name="ck_blood_donations_units_positive"),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    blood_request_uuid: str | None = Field(default=None, foreign_key="blood_requests.uuid")
    donor_profile_uuid: str = Field(foreign_key="donor_profiles.uuid", nullable=False)
    units: int = Field(nullable=False)
    donated_at: datetime = Field(nullable=False, sa_type=UTCDateTime)
    confirmed_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")


# Indexes
Index("idx_donor_profiles_user_uuid", DonorProfile.user_uuid)
Index("idx_donor_profiles_district", DonorProfile.district)
Index("idx_donor_profiles_latitude_longitude", DonorProfile.latitude, DonorProfile.longitude)
Index("idx_blood_requests_requester_user_uuid", BloodRequest.requester_user_uuid)
Index("idx_blood_requests_district", BloodRequest.district)
Index("idx_blood_requests_latitude_longitude", BloodRequest.latitude, BloodRequest.longitude)
Index("idx_blood_request_responses_blood_request_uuid", BloodRequestResponse.blood_request_uuid)
Index("idx_blood_request_responses_donor_profile_uuid", BloodRequestResponse.donor_profile_uuid)
Index("idx_blood_donations_blood_request_uuid", BloodDonation.blood_request_uuid)
Index("idx_blood_donations_donor_profile_uuid", BloodDonation.donor_profile_uuid)
Index("idx_blood_donations_confirmed_by_user_uuid", BloodDonation.confirmed_by_user_uuid)
Index("uq_blood_request_responses_request_donor", BloodRequestResponse.blood_request_uuid, BloodRequestResponse.donor_profile_uuid, unique=True)
