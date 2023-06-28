from uuid import UUID
from typing import Union
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update
from sqlalchemy import select

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
        await self.session.commit()
        return new_mailing

    async def get_mailings(self):
        query = select(Mailing)
        res = await self.session.execute(query)
        from pprint import pprint
        pprint(res.fetchall())
        return None
