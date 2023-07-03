import datetime
from uuid import UUID
from typing import Union
import httpx

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from db.dals import MessageDAL
from settings import TOKEN


class MessageService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_db)
    ):
        self.session = session

    async def update_message(
            self,
            message_id: int,
            message_updated_data: dict
    ) -> Union[UUID, None]:
        async with self.session.begin():
            message_dal = MessageDAL(self.session)
            updated_message_id = await message_dal.update(
                message_id=message_id,
                **message_updated_data
            )
            return updated_message_id

    async def send_message(
            self,
            message_id: int,
            phone_number: str,
            text: str,
            end_datetime: datetime
    ):
        now = datetime.datetime.now(datetime.timezone.utc)
        status = "FAILED"
        if now < end_datetime:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": TOKEN
                }
                response = await client.post(
                    f"https://probe.fbrq.cloud/v1/send/{int(message_id)}",
                    json={
                        "id": int(message_id),
                        "phone": int(phone_number),
                        "text": text
                    },
                    headers=headers
                )
                if response.status_code == 200:
                    status = "SENT"

        print("MESSAGE IS SENT")

        return await self.update_message(
            message_id=message_id,
            message_updated_data={
                "status": status,
                "sending_datetime": now
            }
        )
