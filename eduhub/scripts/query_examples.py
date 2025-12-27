import itertools

from sqlalchemy import desc, select, func
from sqlalchemy.orm import selectin_polymorphic

from eduhub.common.database import get_session
from eduhub.common.config import Config
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
    Resource
)


def main():
    config = Config.load_from_env()
    with get_session(config.postgres_url()) as session:
        accounts_per_laboratories = (
            select(Laboratory, func.count(Account.id).label("account_count"))
            .outerjoin(Account)
            .group_by(Laboratory.id)
            .order_by(func.count(Account.id).asc())
            .limit(1)
        )
        result_first = session.execute(accounts_per_laboratories).scalar_one_or_none()
        print(result_first.__dict__)
        
        top_5_laboratories_by_equipment_amount = (
            select(
                Laboratory, 
                func.count(Equipment.id).label("equipment_count")
            )
            .join(Laboratory.equipment_list)
            .group_by(Laboratory.id)
            .order_by(desc("equipment_count"))
            .limit(5)
        )
        result_second = session.execute(top_5_laboratories_by_equipment_amount).scalars().all()
        for result in result_second:
            print(result.__dict__)

        unique_interests_from_profiles = (
            select(Profile.interest_areas)
        )
        result_third = session.execute(unique_interests_from_profiles).scalars().all()
        result_third = itertools.chain(*result_third)
        result_third = set(result_third)
        print(result_third, len(result_third))

        loader_opt = selectin_polymorphic(Resource, [Dataset, SoftwareRepository, Presentation, Report, Publication])
        one_of_representative_from_resources = select(Resource).order_by(Resource.id).options(loader_opt)
        result_fourth = session.execute(one_of_representative_from_resources).scalars().all()
        for result in result_fourth:
            print(result.__dict__)

if __name__ == "__main__":
    main()
