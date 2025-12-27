from typing import Any
import datetime

from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint, UniqueConstraint, ForeignKey, Table, Column, ARRAY, String, DateTime

from eduhub.common.database import Base


class Laboratory(Base):
    """Scientific-research laboratory, center, or organization ("НИИ" in russian)"""

    __tablename__ = "laboratory"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]

    projects: Mapped[list["Project"]] = relationship(back_populates="laboratory")
    equipment_list: Mapped[list["Equipment"]] = relationship(back_populates="laboratory")
    rooms: Mapped[list["Room"]] = relationship(back_populates="laboratory")
    accounts: Mapped[list["Account"]] = relationship(back_populates="laboratory")


# @TODO: mark publications as optional in m2m
# because they appear only after some time
project_resource = Table(
    "project_resource",
    Base.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("resource_id", ForeignKey("resource.id"), primary_key=True),
    comment="Resources can be reused or shared between different projects (project m2m resource)"
)

project_partner = Table(
    "project_partner",
    Base.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("partner_id", ForeignKey("partner.id"), primary_key=True),
    comment="Partners can participate in multiple projects (project m2m partner)"
)

# i.e., team member, contributer, etc.
# @TODO: role within project (руководитель, исполнитель, и т.д.)
# @TODO: history of activity
# @TODO: constraint to check if person within same laboratory of the project,
# but external consultant can also be part of project
project_participant = Table(
    "project_participant",
    Base.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("account_id", ForeignKey("account.id"), primary_key=True),
    comment="Person can participate in multiple projects (account m2m project)"
)


class Partner(Base):
    """
    Parners or sponsors (individual and legal entity)
    that provides financial and other forms of support
    or to whom we do something (like stakeholders)
    """
    
    __tablename__ = "partner"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    type: Mapped[str] = mapped_column(server_default="local")

    projects: Mapped[list["Project"]] = relationship(secondary=project_partner, back_populates="partners")

    __table_args__ = (
        CheckConstraint("type in ('local', 'regional', 'national', 'international', 'global')"),
    )


# @TODO: budget, duration (from, to), supervisor, funding source, ИРН, and other multiple fields/tables
# @TODO: type enum (type based on financial source and orientation, need to extend)
# @TODO: status enum (status of the project or corresponding phases, need to extend)
# @TODO: content cards in {"en": {}, "ru": {}, "kk": {}} (about_fields as list, tags, info, banner, slogan)
# @TODO: consortium or some form of collaboration between multiple organization (laboratory many-to-many project)
# but for now, we assume that two or many laboratories do not have same research projects (laboratory one-to-many project)
# laboratory_id is mandatory field, because project must be attached to one of them
class Project(Base):
    """Research and development project ("НИОКР" in russian)"""

    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    type: Mapped[str]
    status : Mapped[str]
    # content: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="projects")

    resources: Mapped[list["Resource"]] = relationship(secondary=project_resource, back_populates="projects")
    partners: Mapped[list["Partner"]] = relationship(secondary=project_partner, back_populates="projects")

    __table_args__ = (
        CheckConstraint("type in ('research', 'commercial', 'community')"),
        CheckConstraint("status in ('active', 'completed')"),
    )


# @TODO: decompose to inventory, supply, or assets like in professional inventory management and accounting system
# @TODO: inventory_code like SKU (https://en.wikipedia.org/wiki/Stock_keeping_unit)
# @TODO: generated qr code or bar code
class Equipment(Base):
    """
    Inventory that is available to specific laboratory
    (e.g., physical devices, software licenses, subscriptions, etc.)
    """

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(default="active")
    description: Mapped[str | None]
    image_link: Mapped[str | None] # @TODO: it can be not only "image" (maybe video or mimetype)

    # Some categories of equipment and instances need additional approval requirements (conditions/rules to when, how, why to
    # approve/disapprove). For example, approval by approver (staff member with specific role/position, privilege, areas of responsibility
    # within laboratory, multi-step approval), who is responsible for changing status and management on regular basis. Maybe, laboratory
    # participants can report and message to him about incidents with equipment. Also, approval requirements can
    # define specific days / schedule / time (e.g., working schedule of laboratory or time restrictions).
    # @TODO: approval_requirements are embedded to specific instance of equipment
    # (laboratory can reconfigure it for their own cases independently), 
    # or by equipment_type, or both have affection on it?
    approval_requirements: Mapped[dict[str, Any] | None] = mapped_column(JSONB)

    # laboratory has some equipment and doesn't share it
    # between someone else (laboratory one-to-many equipment)
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="equipment_list")

    # equipment links to one of multiple generic type (equipment many-to-one equipment_type)
    # @TODO: (psycopg.errors.NotNullViolation) null value in column "equipment_type_id"
    # of relation "equipment" violates not-null constraint
    equipment_type_id: Mapped[int | None] = mapped_column(ForeignKey("equipment_type.id"))
    # equipment_type: Mapped["EquipmentType"] = relationship(back_populates="")

    __table_args__ = (
        CheckConstraint("status in ('active', 'malfunctioned', 'maintenance', 'retired')"),
    )


class EquipmentType(Base):
    """
    Lookup/pivot table with possible generic equipment types
    (e.g., USB cable, subcription for coursera, laptop, power adapter, GPU, ...)
    """

    __tablename__ = "equipment_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    characteristics: Mapped[dict[str, Any] | None] = mapped_column(JSONB) # similar to SKU (e.g., brand, model, weight depending on context)


# @TODO: geometric shape and coordinates in postgis
# @TODO: two or more laboratories do not share same space (laboratory one-to-many room).
# But it should be many-to-many to clearly represent cases with external rental spaces.
# Also, need to research about possibility of digital laboratories without any physical space
# within law and regulations of kazakhstan.
class Room(Base):
    """Generic working space or location (office, room, auditorium, building)"""

    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(unique=True) # e.g., name, number, id (like C1.1.111 or in other formats)
    description: Mapped[str | None]
    
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="rooms")


# @TODO: how to mention or attach participants and authors in reasonable way
class Resource(Base):
    """
    Metadata of publication, scientific materials, or works that are developed
    within laboratory (e.g., videos, reports, article, papers, etc.)
    according to list of well-known biblatex/bibtex formats in form
    of polymorhic associations / relationships in order to additional fields or content
    """

    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    link: Mapped[str]
    type: Mapped[str]

    projects: Mapped[list["Project"]] = relationship(secondary=project_resource, back_populates="resources")

    __mapper_args__ = {
        "polymorphic_identity": "resource",
        "polymorphic_on": "type",
    }


# @TODO: quality or resolution and other fields
# @TODO: compatiblity with standard transcription software for subtitles
class Presentation(Resource):
    """Content for presentation (commercial or public)"""

    __tablename__ = "presentation"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    duration: Mapped[int] = mapped_column(server_default="0", comment="Duration in seconds")
    subtitles: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        comment="Subtitles/transcription in different languages and formats",
        # language codes:  {"en": {}, "ru": {}, "kk": {}}
        # format: "SRT", "VTT"
        # by: "automatically_generated", "manually_written"
        # is_verified: bool
    )
    visibility: Mapped[str] = mapped_column(default="private_internal")

    __mapper_args__ = {
        "polymorphic_identity": "presentation",
    }

    __table_args__ = (
        CheckConstraint("visibility in ('private_internal', 'stakeholders_only', 'public_community')"),
    )


class Report(Resource):
    """Regular formal progress report from participant of project"""

    __tablename__ = "report"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    start: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    responsibility_zone: Mapped[str | None]
    comments: Mapped[str | None]
    status: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "report",
    }

    __table_args__ = (
        CheckConstraint("status in ('draft', 'submitted', 'revision', 'approved')"),
    )


class Publication(Resource):
    """Research publication/article on specific topic"""

    __tablename__ = "publication"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1))
    publisher: Mapped[str | None]

    __mapper_args__ = {
        "polymorphic_identity": "publication",
    }


# @TODO: self-referencing to related / similar repositories
# or precomputed/cached query for percent of similarity
class SoftwareRepository(Resource):    
    __tablename__ = "software_repository"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    license: Mapped[str | None]
    lines_amount: Mapped[int] = mapped_column(server_default="0", comment="Amount of source lines of code")

    __mapper_args__ = {
        "polymorphic_identity": "software_repository",
    }


class Dataset(Resource):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    license: Mapped[str | None]
    tags: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1))
    size: Mapped[int] = mapped_column(server_default="0", comment="Total size in bytes")
    # columns_amount: Mapped[int | None]
    # rows_amount: Mapped[int | None]
    attributes: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        comment="Fields/attributes names, description, with corresponding data types"
        # example: ["field_1": {"description": "something explained here", "type": "uint8"}, ...]
    )

    __mapper_args__ = {
        "polymorphic_identity": "dataset",
    }


# @TODO: role within system (moderator, administrator) must be seperated from role within organization
# @TODO: tag, username, and other fields
# @TODO: decompose to multiple full_name to (first_name, middle_name, etc.)
class Account(Base):
    """Account of user in the system"""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str] = mapped_column(server_default="guest", comment="Roles within the system")
    
    # account of user can participate only at one laboratory at a time (laboratory one-to-many account)
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="accounts")

    profile: Mapped["Profile"] = relationship(back_populates="account")

    __table_args__ = (
        CheckConstraint("role in ('guest', 'student', 'staff', 'moderator', 'administrator')"),
    )


# @TODO: some personal information are hidden depending on role
# and visibility configuration like in Steam profile?
# @TODO: age, gender, external links, ...
# @TODO: better define posts as external table
class Profile(Base):
    """Public biography about person (similar to blog page or CV)"""

    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    photo_link: Mapped[str | None]
    description: Mapped[str | None]
    affiliation: Mapped[str | None]
    interest_areas: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1))
    posts: Mapped[dict[str, Any] | None] = mapped_column(JSONB)

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    account: Mapped["Account"] = relationship(back_populates="profile")

    __table_args__ = (
        UniqueConstraint("account_id"),
    )


# @TODO: booking for unlimited time?
# @TODO: constraint for same equipment cannot be booked for approval state is embedded to booking (not as other table)
# @TODO: CHECK the same equipment cannot be booked foroverlapping time intervals
# @TODO: bidirectional connection account ||--|{ booking, equipment ||--|{ booking
# @TODO: add constraint that account of user must belong to laboratory of equipment
# to book one or more equipment (and limit of possible equipments per person)
class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)

    # assume, laboratory shares equipment between their project
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
    requester_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    start: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(server_default="requested")
    
    approver_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    comment: Mapped[str | None]

    booking_histories: Mapped[list["BookingHistory"]] = relationship(back_populates="booking")

    __table_args__ = (
        # CheckConstraint("end > start"), # @TODO: end and start are reserved keywords in postgres (https://www.postgresql.org/docs/current/sql-keywords-appendix.html)
        CheckConstraint("status IN ('requested','approved','rejected','cancelled','completed')"),
    )


# @TODO: trigger to send Booking record after changes to BookingHistory
class BookingHistory(Base):
    """
    History/temporal table for storing usage log for issuing/returning timestamps, 
    condition notes, equipment condition. Similar to version control and it has triggers
    to watch over any changes in Booking table
    """

    __tablename__ = "booking_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    issued_when: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    returned_when: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    note: Mapped[str | None]

    booking_id: Mapped[int] = mapped_column(ForeignKey("booking.id"))
    booking: Mapped["Booking"] = relationship(back_populates="booking_histories")

    __table_args__ = (
        CheckConstraint("returned_when > issued_when"),
    )
