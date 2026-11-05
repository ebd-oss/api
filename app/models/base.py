from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import DateTime, MetaData, TypeDecorator
from sqlmodel import Field, SQLModel


NAMING_CONVENTION = {
    "ix": "idx_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class UTCDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, datetime):
                if value.tzinfo is None:
                    raise ValueError("Naive datetime not allowed")
                value = value.astimezone(timezone.utc).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if isinstance(value, datetime):
                return value.replace(tzinfo=timezone.utc)
        return value


class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        sa_type=UTCDateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        sa_type=UTCDateTime,
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class LocationMixin(SQLModel):
    latitude: float | None = Field(default=None)
    longitude: float | None = Field(default=None)
    division: str | None = Field(default=None)
    district: str | None = Field(default=None)
    upazila: str | None = Field(default=None)
    address_text: str | None = Field(default=None)


class ModerationMixin(SQLModel):
    moderation_status: str = Field(default="pending")
    moderated_by_user_uuid: str | None = Field(default=None)
    moderated_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
