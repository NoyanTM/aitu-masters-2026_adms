import random
import datetime

from sqlalchemy import insert, select
from faker import Faker

from eduhub.common.database import get_session
from eduhub.models import (
    Laboratory,
    Profile,
    Account,
    Room,
    EquipmentType,
    Equipment,
    Project,
    Partner,
    Presentation,
    Report,
    Publication,
    SoftwareRepository,
    Dataset,
    Booking,
)
from eduhub.common.config import Config

# @TODO: generate data beforehand and read from generate data file
# generating list of objects of list of dictionaries
# with get_session(config.postgres_url()) as session:
#     insert_laboratories_statement = (
#         insert(Laboratory)
#         .values(laboratories)
#         .returning(Laboratory.id)
#     )
#     insert_laboratories_results = session.execute(insert_laboratories_statement)
#     insert_laboratories_ids = insert_laboratories_results.scalars().all()

#     # @TODO: how can we sure that they are sorted in same order?
#     for id, project in zip(insert_laboratories_ids, projects):
#         project["laboratory_id"] = id
    
#     insert_projects_statement = (
#         insert(Project)
#         .values(projects)
#         .returning(Project)
#     )
#     insert_projects_results = session.execute(insert_projects_statement)

# @TODO: use factory_boy or polyfactory instead to write
# in declarative format rather than imperative script
def main():
    config = Config.load_from_env()
    fake = Faker()

    MAX_NUM_ACCOUNTS = 20
    MAX_NUM_LABORATORIES = 10
    MAX_NUM_ROOMS_PER_LABORATORY = 5
    MAX_NUM_EQUIPMENT_TYPE = 50
    MAX_NUM_FIELDS_IN_CHARACTERISTICS = 10
    MAX_NUM_EQUIPMENT_PER_LABORATORY = 25
    MAX_NUM_PROJECTS_PER_LABORATORY = 5
    MAX_NUM_PARTNERS_PER_PROJECT = 3
    MAX_NUM_RESOURCES_PER_PROJECT = 5
    MAX_NUM_BOOKINGS = 20
    
    laboratories = [
        Laboratory(title=fake.company(), description=fake.catch_phrase())
        for index in range(1, MAX_NUM_LABORATORIES + 1)
    ]
    rooms = [
        Room(
            label=fake.bothify("C#.#.###"),
            description=fake.text(max_nb_chars=100),
            laboratory=laboratory
        )
        for laboratory in laboratories
        for index in range(1, MAX_NUM_ROOMS_PER_LABORATORY + 1)
    ]
    profiles = [
        Profile(
            photo_link=fake.image_url(),
            description=fake.text(max_nb_chars=100),
            affiliation=fake.company(),
            interest_areas=[fake.job() for index in range(1, random.randint(2, 10))],
            posts=[
                {
                    "slug": fake.slug(),
                    "content": fake.text(max_nb_chars=250),
                    "tags": fake.words(nb=5),
                    "views": random.randint(0, 100)
                }
                for index in range(1, random.randint(2, 10))
            ],
        )
        for index in range(1, MAX_NUM_ACCOUNTS + 1)
    ]
    accounts = [
        Account(
            full_name=fake.name(), # @TODO: faker.full_name
            email=fake.email(), # @TODO: email unique in faker
            role="guest", # @TODO: different roles within system (faker.enum)
            laboratory=random.choice(laboratories), # @TODO: choosing distribution of random and rarity 
        )
        for index in range(1, MAX_NUM_ACCOUNTS + 1)
    ]
    equipment_types = [
        EquipmentType(
            title=fake.catch_phrase(), # @TODO: generate from list of laboratory equipment or scientific related
            description=fake.text(max_nb_chars=200),
            characteristics={
                f"field_{index}": random.choice([
                    fake.pyint(min_value=1, max_value=100),
                    fake.pystr(min_chars=1, max_chars=100),
                    fake.pyfloat(left_digits=3, right_digits=2),
                    fake.pybool(truth_probability=50),
                ])
                for index in range(1, MAX_NUM_FIELDS_IN_CHARACTERISTICS + 1)   
            }
        )
        for index in range(1, MAX_NUM_EQUIPMENT_TYPE + 1)
    ]
    equipment_list = [
        Equipment(
            status="active", # @TODO: enum
            description=fake.text(max_nb_chars=200),
            image_link=fake.image_url(),
            approval_requirements={"minimal_role": "assistant"}, # @TODO: enum and other rule-fields
            laboratory=laboratory,
        )
        for laboratory in laboratories
        for index in range(1, MAX_NUM_EQUIPMENT_PER_LABORATORY + 1)
    ]
    projects = [
        Project(
            title=fake.text(max_nb_chars=20),
            description=fake.text(max_nb_chars=200),
            type="research", # @TODO: enum
            status="active", # @TODO: enum
            laboratory=laboratory
        )
        for laboratory in laboratories
        for index in range(1, random.randint(2, MAX_NUM_PROJECTS_PER_LABORATORY + 1))
    ]
    partners = [
        Partner(
            title=fake.company(),
            type="local",
            projects=projects
        )
        for project in projects
        for index in range(1, random.randint(2, MAX_NUM_PARTNERS_PER_PROJECT + 1))
    ]
    resources = [
        random.choice(
            [
                Presentation(
                    title=fake.text(max_nb_chars=20),
                    description=fake.text(max_nb_chars=200),
                    link=fake.url(),
                    duration=fake.pyint(min_value=1, max_value=10**5),
                    visibility="private_internal",
                    subtitles=[
                        {   
                            "format": "VTT",
                            "language_code": "en",
                            "content": fake.text(max_nb_chars=200),
                            "is_verified": fake.pybool(truth_probability=50),
                            "by": "automatically_generated",
                        }
                        for index in range(1, 5)
                    ]
                ),
                Report(
                    title=fake.text(max_nb_chars=20),
                    description=fake.text(max_nb_chars=200),
                    link=fake.url(),
                    start=datetime.datetime.now(tz=datetime.UTC),
                    end=datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(seconds=random.randint(100, 10**4)),
                    responsibility_zone=fake.text(max_nb_chars=200),
                    comments=fake.text(max_nb_chars=200),
                    status="draft",
                    projects=projects,
                ),
                Publication(
                    title=fake.text(max_nb_chars=20),
                    description=fake.text(max_nb_chars=200),
                    link=fake.url(),
                    keywords=fake.words(nb=5),
                    publisher=fake.company(),
                    projects=projects,
                ),
                SoftwareRepository(
                    title=fake.text(max_nb_chars=20),
                    description=fake.text(max_nb_chars=200),
                    link=fake.url(),
                    license=fake.text(max_nb_chars=20),
                    lines_amount=fake.pyint(min_value=1, max_value=10**4),
                    projects=projects,
                ),
                Dataset(
                    title=fake.text(max_nb_chars=20),
                    description=fake.text(max_nb_chars=200),
                    link=fake.url(),
                    license=fake.text(max_nb_chars=20),
                    tags=fake.words(nb=5),
                    size=fake.pyint(min_value=1, max_value=10**4),
                    attributes={
                        f"field_{index}": {
                            "description": fake.text(max_nb_chars=100),
                            "type": fake.mime_type()
                        }
                        for index in range(1, 10 + 1)
                    },
                    projects=projects,
                )
            ]
        )
        for index in range(1, random.randint(2, MAX_NUM_RESOURCES_PER_PROJECT + 1))
    ]
    booking = [
        Booking(
            start=datetime.datetime.now(tz=datetime.UTC),
            end=datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(seconds=random.randint(100, 10**4)),
            status="requested",
            comment=fake.text(max_nb_chars=200),
        )
        for index in range(1, MAX_NUM_BOOKINGS + 1)
    ]

    with get_session(config.postgres_url()) as session:
        session.add_all(laboratories)
        session.add_all(accounts)
        session.add_all(rooms)
        session.add_all(equipment_types)
        session.flush()
        
        account_ids = [account.id for account in accounts]
        for account_id, profile in zip(account_ids, profiles):
            setattr(profile, "account_id", account_id)
        session.add_all(profiles)
        session.flush()

        equipment_types_ids = [equipment_type.id for equipment_type in equipment_types]
        for equipment_element in equipment_list:
            setattr(equipment_element, "equipment_type_id", random.choice(equipment_types_ids))
        session.add_all(equipment_list)

        session.add_all(projects)
        session.flush()

        session.add_all(partners)
        session.add_all(resources)
        session.flush()
        
        # equipment_id: Mapped[int] = mapped_column(ForeignKey("equipment.id"))
        # requester_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
        # approver_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
        # session.add_all(booking)
        # session.flush()
        
        session.commit()


if __name__ == "__main__":
    main()
