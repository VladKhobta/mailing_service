import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Recipient(Base):

    __tablename__ = 'recipients'

    recipient_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    phone_number = Column(
        String,
        nullable=False,
        unique=True
    )
    mobile_code = Column(
        String,
        nullable=False
    )  # from phone number
    time_zone = Column(
        String,
        nullable=False
    )
    tag = Column(
        String,
        nullable=True
    )

