from datetime import datetime, timezone, timedelta
from random import randint

from eduhub.common.config import Config
from eduhub.common.database import get_session
from eduhub.common.types import BookingStatus
from eduhub.models import Booking

from sqlalchemy.exc import SQLAlchemyError

def main():
    config = Config.load_from_env()
    random_condition = randint(1, 10)
    with get_session(config.postgres_url()) as session:
        booking_obj = Booking(
            equipment_id=1,
            requester_id=2,
            approver_id=3,
            start_ts=datetime.now(tz=timezone.utc),
            end_ts=datetime.now(tz=timezone.utc) + timedelta(days=2),
            status=BookingStatus.REQUESTED,
            comment="Initial booking request",
        )
        session.add(booking_obj)
        
        booking_obj = Booking(
            equipment_id=3,
            requester_id=4,
            approver_id=5,
            start_ts=datetime.now(tz=timezone.utc),
            end_ts=datetime.now(tz=timezone.utc) + timedelta(days=2),
            status="123", # incorrect
            comment="Other booking request",
        )
        session.add(booking_obj)

        session.commit()


if __name__ == "__main__":
    main()
