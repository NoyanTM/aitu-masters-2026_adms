from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from eduhub.common.config import Config
from eduhub.common.database import get_session
from eduhub.common.types import BookingStatus
from eduhub.models import Booking

def main():
    config = Config.load_from_env()
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
        session.flush()

        booking = session.scalar(
            select(Booking).where(Booking.id == booking_obj.id)
        )
        if booking is None:
            raise ValueError("Booking not found")

        booking.status = BookingStatus.APPROVED
        booking.approver_id = 5
        booking.comment = "Approved by lab manager"
        booking.end_ts = datetime.now(tz=timezone.utc)

        session.commit()


if __name__ == "__main__":
    main()
