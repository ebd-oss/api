from datetime import datetime
from uuid import uuid4

from sqlalchemy import Index, text
from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin, UTCDateTime


class IdentityVerification(TimestampMixin, SQLModel, table=True):
    __tablename__ = "identity_verifications"
    __table_args__ = (
        Index(
            "idx_identity_verifications_method_doc_hash_verified",
            "method",
            "document_hash",
            unique=True,
            sqlite_where=text("status = 'verified'"),
        ),
        Index(
            "idx_identity_verifications_person_ref_verified",
            "person_reference_hash",
            unique=True,
            sqlite_where=text("status = 'verified' AND person_reference_hash IS NOT NULL"),
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    method: str = Field(nullable=False)
    status: str = Field(nullable=False)
    document_hash: str = Field(nullable=False)
    person_reference_hash: str | None = Field(default=None)
    provider_reference: str | None = Field(default=None)
    verified_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    failure_code: str | None = Field(default=None)
    attempt_number: int = Field(default=1)

from sqlalchemy import Index

Index("idx_identity_verifications_user_uuid", IdentityVerification.user_uuid)
