from uuid import UUID
from typing import Union, List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select, func

from db.models.mailing import Mailing
from schemas.mailings import (
    ShowMailing
)


class MailingDAL:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            start_datetime: datetime,
            end_datetime: datetime,
            content: str,
            tag_filter: str,
            mobile_code_filter: str
    ) -> Mailing:
        new_mailing = Mailing(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            content=content,
            tag_filter=tag_filter,
            mobile_code_filter=mobile_code_filter
        )
        self.session.add(new_mailing)
        await self.session.flush()
        return new_mailing

    async def update(
            self,
            mailing_id: UUID,
            **kwargs
    ) -> Union[UUID, None]:
        query = (
            update(Mailing)
            .where(Mailing.mailing_id == mailing_id)
            .values(kwargs)
            .returning(Mailing.mailing_id)
        )
        res = await self.session.execute(query)
        updated_mailing_row = res.fetchone()
        if updated_mailing_row:
            return updated_mailing_row[0]

    async def delete(
            self,
            mailing_id: UUID
    ) -> Union[UUID, None]:
        query = (
            delete(Mailing)
            .where(Mailing.mailing_id == mailing_id)
            .returning(Mailing.mailing_id)
        )
        res = await self.session.execute(query)
        deleted_mailing_row = res.fetchone()
        if deleted_mailing_row:
            return deleted_mailing_row[0]

    async def get_mailing_by_id(
            self,
            mailing_id: UUID
    ) -> Union[Mailing, None]:
        query = (
            select(Mailing)
            .where(Mailing.mailing_id == mailing_id)
        )
        res = await self.session.execute(query)

        return res.scalar()

    async def get_mailings(self) -> int:
        query = select(Mailing)
        res = await self.session.execute(query)

        return res.scalars().all()

    async def get_mailings_count(self) -> int:
        query = select(func.count()).select_from(Mailing)
        res = await self.session.execute(query)
        return res.scalar()
