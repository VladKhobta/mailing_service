import uuid

from sqlalchemy import (
    Column, Enum, DateTime, Integer
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
import enum


class MessageStatus(enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Message(Base):

    __tablename__ = "messages"

    message_id = Column(
        Integer,
        primary_key=True,
    )
    sending_datetime = Column(
        DateTime(timezone=True),
        nullable=True
    )
    status = Column(
        Enum(MessageStatus),
        default=MessageStatus.PENDING
    )
    recipient_id = Column(
        UUID(as_uuid=True),
        ForeignKey("recipients.recipient_id")
    )
    mailing_id = Column(
        UUID(as_uuid=True),
        ForeignKey("mailings.mailing_id")
    )

    mailing = relationship("Mailing", backref="messages")
    recipient = relationship("Recipient", backref="messages")
