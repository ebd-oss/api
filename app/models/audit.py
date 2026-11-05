from datetime import datetime
from uuid import uuid4

from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin, UTCDateTime


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_logs"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    actor_user_uuid: str | None = Field(default=None)
    actor_account_type: str | None = Field(default=None)
    institution_uuid: str | None = Field(default=None)  # no FK
    action: str = Field(nullable=False)
    permission_code: str | None = Field(default=None)
    entity_type: str = Field(nullable=False)
    entity_uuid: str = Field(nullable=False)  # polymorphic, no FK
    previous_values: str | None = Field(default=None)  # JSON stored as text
    new_values: str | None = Field(default=None)  # JSON stored as text
    environment: str | None = Field(default=None)
    trace_id: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=UTCDateTime,
        nullable=False,
    )
