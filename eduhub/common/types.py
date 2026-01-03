import enum


class AccountRole(enum.StrEnum):
    GUEST = enum.auto()
    STUDENT = enum.auto()
    STAFF = enum.auto()
    MODERATOR = enum.auto()
    ADMINISTRATOR = enum.auto()


class PartnerType(enum.StrEnum):
    LOCAL = enum.auto()
    REGIONAL = enum.auto()
    NATIONAL = enum.auto()
    INTERNATIONAL = enum.auto()
    GLOBAL = enum.auto()


class ProjectType(enum.StrEnum):
    """Type of the project based on financial source, context, or orientation"""
    RESEARCH = enum.auto()
    COMMERCIAL = enum.auto()
    COMMUNITY = enum.auto()


class ProjectStatus(enum.StrEnum):
    """Status of the project with itscorresponding phases"""
    ACTIVE = enum.auto()
    COMPLETED = enum.auto()


class EquipmentStatus(enum.StrEnum):
    ACTIVE = enum.auto()
    MALFUNCTIONED = enum.auto()
    MAINTENANCE = enum.auto()
    RETIRED = enum.auto()


class BookingStatus(enum.StrEnum):
    REQUESTED = enum.auto()
    APPROVED = enum.auto()
    REJECTED = enum.auto()
    CANCELLED = enum.auto()
    COMPLETED = enum.auto()


class ReportStatus(enum.StrEnum):
    DRAFT = enum.auto()
    SUBMITTED = enum.auto()
    REVISION = enum.auto()
    APPROVED = enum.auto()


class PresentationVisibility(enum.StrEnum):
    PRIVATE_INTERNAL = enum.auto()
    STAKEHOLDERS_ONLY = enum.auto()
    PUBLIC_COMMUNITY = enum.auto()
