from uuid import uuid4

from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin


class MediaFile(TimestampMixin, SQLModel, table=True):
    __tablename__ = "media_files"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    uploaded_by_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    storage_path: str = Field(nullable=False)
    mime_type: str = Field(nullable=False)
    size_bytes: int = Field(nullable=False)
    sha256: str = Field(nullable=False)
    width: int | None = Field(default=None)
    height: int | None = Field(default=None)

from sqlalchemy import Index

Index("idx_media_files_uploaded_by_user_uuid", MediaFile.uploaded_by_user_uuid)
