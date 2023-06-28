import uuid

from sqlalchemy import (
    Column, String, DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint

from .base import Base


class Mailing(Base):

    __tablename__ = "mailings"

    mailing_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    start_datetime = Column(
        DateTime(timezone=True),
        nullable=False
    )
    end_datetime = Column(
        DateTime(timezone=True),
        nullable=False
    )
    content = Column(
        String,
        nullable=False
    )
    tag_filter = Column(
        String,
    )
    mobile_code_filter = Column(
        String,
    )

    __table_args__ = (
        CheckConstraint(
            "(tag_filter IS NOT NULL OR mobile_code_filter IS NOT NULL)",
            name="one_filter_is_not_null"
        ),
        CheckConstraint(
            'start_datetime <= end_datetime',
            name='check_start_end_datetime'
        )
    )
