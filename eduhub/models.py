from typing import Any
import datetime

from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import (
    CheckConstraint, 
    UniqueConstraint,
    ForeignKey,
    Table,
    Column,
    ARRAY,
    String,
    DateTime,
    event,
    inspect,
)

from eduhub.common.database import Base
from eduhub.common.types import (
    AccountRole, 
    PartnerType,
    PresentationVisibility, 
    ProjectType,
    ProjectStatus,
    EquipmentStatus,
    BookingStatus,
    ReportStatus,
)

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
    type: Mapped[PartnerType] = mapped_column(default=PartnerType.LOCAL)

    projects: Mapped[list["Project"]] = relationship(secondary=project_partner, back_populates="partners")


class Project(Base):
    """Research and development project ("НИОКР" in russian)"""

    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    type: Mapped[ProjectType] = mapped_column(default=ProjectType.RESEARCH)
    status : Mapped[ProjectStatus] = mapped_column(default=ProjectStatus.ACTIVE)

    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="projects")

    resources: Mapped[list["Resource"]] = relationship(secondary=project_resource, back_populates="projects")
    partners: Mapped[list["Partner"]] = relationship(secondary=project_partner, back_populates="projects")
    participants: Mapped[list["Account"]] = relationship(secondary=project_participant, back_populates="projects")


class Equipment(Base):
    """
    Inventory that is available to specific laboratory
    (e.g., physical devices, software licenses, subscriptions, etc.)
    """

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[EquipmentStatus] = mapped_column(default=EquipmentStatus.ACTIVE)
    description: Mapped[str | None]
    media_link: Mapped[str | None] = mapped_column(comment="video, image, audio, or other mimetype")
    approval_requirements: Mapped[dict[str, Any] | None] = mapped_column(JSONB)

    # laboratory has some equipment and doesn't share it between someone else (laboratory one-to-many equipment)
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="equipment_list")

    # equipment links to one of multiple generic type (equipment many-to-one equipment_type)
    equipment_type_id: Mapped[int | None] = mapped_column(ForeignKey("equipment_type.id"))
    # equipment_type: Mapped["EquipmentType"] = relationship(back_populates="")


class EquipmentType(Base):
    """
    Lookup/pivot table with possible generic equipment types
    (e.g., USB cable, subcription for coursera, laptop, power adapter, GPU, ...)
    """

    __tablename__ = "equipment_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    characteristics: Mapped[dict[str, Any] | None] = mapped_column(JSONB, comment="similar to SKU (e.g., brand, model, weight depending on the context)")


class Room(Base):
    """Generic working space or location (office, room, auditorium, building)"""

    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(unique=True, comment="name, number, id (like C1.1.111 or in other formats)")
    description: Mapped[str | None]
    
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="rooms")


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
    visibility: Mapped[PresentationVisibility] = mapped_column(default=PresentationVisibility.PRIVATE_INTERNAL)

    __mapper_args__ = {
        "polymorphic_identity": "presentation",
    }


class Report(Resource):
    """Regular formal progress report from participant of project"""

    __tablename__ = "report"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    start: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    responsibility_zone: Mapped[str | None]
    comments: Mapped[str | None]
    status: Mapped[ReportStatus] = mapped_column(default=ReportStatus.DRAFT)

    __mapper_args__ = {
        "polymorphic_identity": "report",
    }


class Publication(Resource):
    """Research publication/article on specific topic"""

    __tablename__ = "publication"

    id: Mapped[int] = mapped_column(ForeignKey("resource.id"), primary_key=True)
    keywords: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1))
    publisher: Mapped[str | None]

    __mapper_args__ = {
        "polymorphic_identity": "publication",
    }


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
    attributes: Mapped[dict[str, Any] | None] = mapped_column(
        JSONB,
        comment="Fields/attributes names, description, with corresponding data types"
        # example: ["field_1": {"description": "something explained here", "type": "uint8"}, ...]
    )

    __mapper_args__ = {
        "polymorphic_identity": "dataset",
    }


class Account(Base):
    """Account of user in the system"""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    role: Mapped[AccountRole] = mapped_column(default=AccountRole.GUEST, comment="Role within the system")
    
    # account of user can participate only at one laboratory at a time (laboratory one-to-many account)
    laboratory_id: Mapped[int] = mapped_column(ForeignKey("laboratory.id"))
    laboratory: Mapped["Laboratory"] = relationship(back_populates="accounts")

    profile: Mapped["Profile"] = relationship(back_populates="account")
    projects: Mapped[list["Project"]] = relationship(secondary=project_participant, back_populates="participants")


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


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)

    # laboratory shares their regular equipment between their project
    equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
    requester_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    start_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True)) # issued_when
    end_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True)) # returned_when
    status: Mapped[BookingStatus] = mapped_column(default=BookingStatus.REQUESTED)
    
    approver_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    comment: Mapped[str | None]

    booking_histories: Mapped[list["BookingHistory"]] = relationship(back_populates="booking")

    __table_args__ = (
        CheckConstraint("end_ts > start_ts"),
    )


class BookingHistory(Base):
    """
    History/temporal table for storing usage log for issuing/returning timestamps, 
    condition notes, equipment condition. Similar to version control and it has triggers
    to watch over any changes in Booking table
    """

    __tablename__ = "booking_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[str | None]
    changed_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    booking_id: Mapped[int] = mapped_column(ForeignKey("booking.id"))
    booking: Mapped["Booking"] = relationship(back_populates="booking_histories")


@event.listens_for(Booking, "after_insert")
@event.listens_for(Booking, "after_update")
@event.listens_for(Booking, "after_delete")
def booking_history_event(mapper, connection, target: Booking):
    session = Session.object_session(target)
    if session is None:
        return
    note = "Booking changed"
    if mapper.dispatch.after_update:
        state = inspect(target)
        changed = [
            attr.key
            for attr in state.attrs
            if attr.history.has_changes()
        ]
        if changed:
            note = f"Updated fields: {', '.join(changed)}"
    history = BookingHistory(
        booking_id=target.id,
        changed_at=datetime.datetime.now(tz=datetime.timezone.utc),
        note=note,
    )
    session.add(history)
