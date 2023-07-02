from typing import Union
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.recipients import RecipientCreate, ShowRecipient
from db.dals.recipients import RecipientDAL
from db.session import get_db


class RecipientService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_db)
    ):
        self.session = session

    async def get_by_id(
            self,
            recipient_id: UUID
    ):
        async with self.session.begin():
            recipient_dal = RecipientDAL(self.session)
            recipient = await recipient_dal.get_by_id(
                recipient_id=recipient_id
            )
            return recipient


    async def create(
            self,
            body: RecipientCreate
    ) -> ShowRecipient:
        async with self.session.begin():
            recipient_dal = RecipientDAL(self.session)
            mobile_code = body.phone_number[1:4]
            recipient = await recipient_dal.create(
                phone_number=body.phone_number,
                mobile_code=mobile_code,
                time_zone=body.time_zone,
                tag=body.tag
            )
            return ShowRecipient(
                recipient_id=recipient.recipient_id,
                phone_number=recipient.phone_number,
                mobile_code=recipient.mobile_code,
                time_zone=recipient.time_zone,
                tag=recipient.tag
            )


    async def delete(
        self,
        recipient_id: UUID,
    ) -> Union[UUID, None]:
        async with self.session.begin():
            recipient_dal = RecipientDAL(self.session)
            deleted_recipient_id = await recipient_dal.delete(
                recipient_id=recipient_id,
            )
            return deleted_recipient_id

    async def update(
            self,
            recipient_id: UUID,
            recipient_updated_data: dict
    ) -> Union[UUID, None]:
        async with self.session.begin():
            recipient_dal = RecipientDAL(self.session)
            updated_recipient_id = await recipient_dal.update(
                recipient_id=recipient_id,
                **recipient_updated_data
            )
            return updated_recipient_id
