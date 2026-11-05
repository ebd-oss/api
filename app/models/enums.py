from enum import StrEnum


class AccountType(StrEnum):
    INDIVIDUAL = "individual"
    INSTITUTION_ADMIN = "institution_admin"
    INSTITUTION_STAFF = "institution_staff"
    SPONSOR = "sponsor"
    EBD_ADMIN = "ebd_admin"
    SUPER_ADMIN = "super_admin"


class UserStatus(StrEnum):
    PENDING_VERIFICATION = "pending_verification"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"
    DEACTIVATED = "deactivated"


class OtpChannel(StrEnum):
    SMS = "sms"
    EMAIL = "email"


class OtpPurpose(StrEnum):
    REGISTRATION = "registration"
    LOGIN = "login"
    PASSWORD_RESET = "password_reset"
    PHONE_VERIFY = "phone_verify"
    EMAIL_VERIFY = "email_verify"


class IdentityMethod(StrEnum):
    NATIONAL_ID = "national_id"
    PASSPORT = "passport"
    BIRTH_REGISTRATION = "birth_registration"


class IdentityStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class PermissionAction(StrEnum):
    VIEW = "view"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    MODERATE = "moderate"
    APPROVE = "approve"
    ASSIGN = "assign"
    EXPORT = "export"
    SEND = "send"
    ADMINISTER = "administer"


class ModerationStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
