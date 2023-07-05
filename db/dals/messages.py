import enum
from uuid import UUID
from typing import Union, Optional, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from db.models import Message
from db.models.messages import MessageStatus

from services.scheduling import scheduler


class MessageDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            status: MessageStatus,
            mailing_id: UUID,
            recipient_id: UUID,
            sending_datetime: Optional[datetime] = None
    ):
        message = Message(
            status=status,
            sending_datetime=sending_datetime,
            recipient_id=recipient_id,
            mailing_id=mailing_id
        )
        self.session.add(message)
        await self.session.flush()
        return message

    async def get_by_id(
            self,
            message_id: int
    ) -> Union[Message, None]:
        query = select(Message).where(Message.message_id == message_id)
        res = await self.session.execute(query)
        message_row = res.fetchone()
        if message_row:
            return message_row[0]

    async def delete_related_to_mailing(
            self,
            mailing_id: UUID
    ):
        messages = await self.session.execute(
            select(Message)
            .where(Message.mailing_id == mailing_id)
        )
        messages = messages.scalars().all()

        if messages is not None:
            for message in messages:
                if message.status == "PENDING":
                    print('deleting job')
                    scheduler.remove_job(str(message.message_id))
                await self.session.delete(message)

    async def update(
            self,
            message_id: int,
            **kwargs
    ) -> Union[int, None]:
        query = (
            update(Message)
            .where(Message.message_id == message_id)
            .values(kwargs)
            .returning(Message.message_id)
        )
        res = await self.session.execute(query)
        updated_message_row = res.fetchone()
        if updated_message_row:
            return updated_message_row[0]

    async def get_status_count(self, status: MessageStatus):
        status_count = await self.session.execute(
            select(func.count())
            .where(Message.status == status)
        )
        return status_count.scalar()

    async def get_status_count_detailed(
            self,
            status: MessageStatus,
            mailing_id: UUID
    ):
        status_count = await self.session.execute(
            select(func.count())
            .where(Message.mailing_id == mailing_id)
            .where(Message.status == status)
        )
        return status_count.scalar()

    async def get_messages_ids(
            self,
            mailing_id: UUID
    ) -> List[int]:
        query = (
            select(Message)
            .where(Message.mailing_id == mailing_id)
        )
        res = await self.session.execute(query)
        return [message.message_id for message in res.scalars()]
