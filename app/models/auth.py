from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint
from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin, UTCDateTime


class OtpChallenge(TimestampMixin, SQLModel, table=True):
    __tablename__ = "otp_challenges"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    channel: str = Field(nullable=False)
    target: str = Field(nullable=False)
    purpose: str = Field(nullable=False)
    code_hash: str = Field(nullable=False)
    expires_at: datetime = Field(nullable=False, sa_type=UTCDateTime)
    attempts: int = Field(default=0)
    max_attempts: int = Field(default=5)
    consumed_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    user_uuid: str | None = Field(default=None, foreign_key="users.uuid")


class RefreshToken(TimestampMixin, SQLModel, table=True):
    __tablename__ = "refresh_tokens"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    token_hash: str = Field(nullable=False, unique=True)
    expires_at: datetime = Field(nullable=False, sa_type=UTCDateTime)
    revoked_at: datetime | None = Field(default=None, sa_type=UTCDateTime)

from sqlalchemy import Index

Index("idx_otp_challenges_user_uuid", OtpChallenge.user_uuid)
Index("idx_refresh_tokens_user_uuid", RefreshToken.user_uuid)
