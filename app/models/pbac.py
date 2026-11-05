from datetime import datetime
from uuid import uuid4

from sqlalchemy import CheckConstraint
from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin, UTCDateTime


class Permission(TimestampMixin, SQLModel, table=True):
    __tablename__ = "permissions"
    __table_args__ = (
        CheckConstraint(
            "action IN ('view','create','update','delete','moderate','approve','assign','export','send','administer')",
            name="ck_permissions_action",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    code: str = Field(nullable=False, unique=True)
    resource: str = Field(nullable=False)
    action: str = Field(nullable=False)


class PermissionGroup(TimestampMixin, SQLModel, table=True):
    __tablename__ = "permission_groups"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    is_template: bool = Field(default=False)


class PermissionGroupPermission(TimestampMixin, SQLModel, table=True):
    __tablename__ = "permission_group_permissions"

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    permission_group_uuid: str = Field(foreign_key="permission_groups.uuid", nullable=False)
    permission_uuid: str = Field(foreign_key="permissions.uuid", nullable=False)


class UserPermissionGrant(TimestampMixin, SQLModel, table=True):
    __tablename__ = "user_permission_grants"
    __table_args__ = (
        CheckConstraint(
            "(permission_uuid IS NOT NULL AND permission_group_uuid IS NULL) OR (permission_uuid IS NULL AND permission_group_uuid IS NOT NULL)",
            name="ck_user_permission_grants_exactly_one",
        ),
    )

    uuid: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    permission_uuid: str | None = Field(default=None, foreign_key="permissions.uuid")
    permission_group_uuid: str | None = Field(default=None, foreign_key="permission_groups.uuid")
    granted_by_user_uuid: str = Field(foreign_key="users.uuid", nullable=False)
    purpose: str = Field(nullable=False)
    expires_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    revoked_at: datetime | None = Field(default=None, sa_type=UTCDateTime)
    revoked_by_user_uuid: str | None = Field(default=None, foreign_key="users.uuid")
    revoke_reason: str | None = Field(default=None)
    institution_uuid: str | None = Field(default=None)  # no FK - lands with institutions table

from sqlalchemy import Index

Index("idx_permission_group_permissions_permission_group_uuid", PermissionGroupPermission.permission_group_uuid)
Index("idx_permission_group_permissions_permission_uuid", PermissionGroupPermission.permission_uuid)
Index("idx_user_permission_grants_user_uuid", UserPermissionGrant.user_uuid)
Index("idx_user_permission_grants_permission_uuid", UserPermissionGrant.permission_uuid)
Index("idx_user_permission_grants_permission_group_uuid", UserPermissionGrant.permission_group_uuid)
Index("idx_user_permission_grants_granted_by_user_uuid", UserPermissionGrant.granted_by_user_uuid)
Index("idx_user_permission_grants_revoked_by_user_uuid", UserPermissionGrant.revoked_by_user_uuid)
