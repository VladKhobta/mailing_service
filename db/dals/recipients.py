from uuid import UUID
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select

from db.models.recipients import Recipient


class RecipientDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
            self,
            recipient_id: UUID
    ) -> Union[Recipient, None]:
        query = select(Recipient).where(Recipient.recipient_id == recipient_id)
        res = await self.session.execute(query)
        recipient_row = res.fetchone()
        if recipient_row is not None:
            return recipient_row[0]

    async def create(
            self,
            phone_number: str,
            mobile_code: str,
            time_zone: str,
            tag: str,
    ) -> Recipient:
        new_recipient = Recipient(
            phone_number=phone_number,
            mobile_code=mobile_code,
            time_zone=time_zone,
            tag=tag
        )
        self.session.add(new_recipient)
        await self.session.commit()
        return new_recipient

    async def delete(
            self,
            recipient_id: UUID
    ) -> Union[UUID, None]:
        query = (
            delete(Recipient)
            .where(Recipient.recipient_id == recipient_id)
            .returning(Recipient.recipient_id)
        )
        res = await self.session.execute(query)
        deleted_recipient_row = res.fetchone()
        if deleted_recipient_row is not None:
            return deleted_recipient_row[0]

    async def update(
            self,
            recipient_id: UUID,
            **kwargs
    ) -> Union[UUID, None]:
        query = (
            update(Recipient)
            .where(Recipient.recipient_id == recipient_id)
            .values(kwargs)
            .returning(Recipient.recipient_id)
        )
        res = await self.session.execute(query)
        updated_recipient_row = res.fetchone()
        if updated_recipient_row is not None:
            return updated_recipient_row[0]
