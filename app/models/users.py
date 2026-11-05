from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin, UTCDateTime


class User(TimestampMixin, SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "(email IS NOT NULL AND email != '') OR (phone IS NOT NULL AND phone != '')",
            name="ck_users_email_or_phone",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    ebd_id: str | None = Field(default=None, unique=True)
    account_type: str = Field(nullable=False)
    status: str = Field(nullable=False)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    password_hash: str | None = Field(default=None)
    email_verified_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    phone_verified_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    last_login_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    deleted_at: datetime | None = Field(default=None, sa_type=UTCDateTime)

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("phone", name="uq_users_phone"),
        CheckConstraint(
            "(email IS NOT NULL AND email != '') OR (phone IS NOT NULL AND phone != '')",
            name="ck_users_email_or_phone",
        ),
    )


class UserProfile(TimestampMixin, SQLModel, table=True):
    __tablename__ = "user_profiles"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False, unique=True)
    display_name: str | None = Field(default=None)
    photo_media_uuid: str | None = Field(default=None)


class UserPrivateDetail(TimestampMixin, SQLModel, table=True):
    __tablename__ = "user_private_details"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False, unique=True)
    legal_name: str | None = Field(default=None)
    date_of_birth: datetime | None = Field(default=None, sa_type=UTCDateTime)
    address: str | None = Field(default=None)


# Add indexes for FKs
from sqlalchemy import Index

Index("idx_user_profiles_user_uuid", UserProfile.user_uuid)
Index("idx_user_private_details_user_uuid", UserPrivateDetail.user_uuid)
