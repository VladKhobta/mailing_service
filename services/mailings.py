from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals.mailings import MailingDAL
from db.session import get_db
from schemas.mailings import (
    ShowMailing,
    MailingCreate
)

from sch import scheduler


async def send_notification(recipient, message):
    # Реализуйте здесь логику отправки уведомления
    print(f"Sending notification to {recipient}: {message}")
    # коннект к внешнему сервису и отправка


async def process_delivery(delivery_id):
    # Находим рассылку по ID в вашем хранилище
    # (здесь просто выводим сообщение для наглядности)
    print(f"Processing delivery {delivery_id}")
    # сбор тех, кому надо это все отправить и отправка каждому
    await send_notification('vlad', 'hi!')


class MailingService:

    def __init__(
            self,
            session: AsyncSession = Depends(get_db)
    ):
        self.session = session

    async def create(
            self,
            body: MailingCreate,
    ) -> ShowMailing:
        async with self.session.begin():
            mailing_dal = MailingDAL(self.session)
            mailing = await mailing_dal.create(
                start_datetime=body.start_datetime,
                end_datetime=body.end_datetime,
                content=body.content,
                tag_filter=body.tag_filter,
                mobile_code_filter=body.mobile_code_filter
            )
            print(body.start_datetime)

            scheduler.add_job(
                process_delivery,
                args=['chch'],
                run_date=body.start_datetime
            )

            return ShowMailing(
                mailing_id=mailing.mailing_id,
                start_datetime=mailing.start_datetime,
                end_datetime=mailing.end_datetime,
                content=mailing.content,
                tag_filter=mailing.tag_filter,
                mobile_code_filter=mailing.mobile_code_filter
            )


    async def get_mailings(self):
        async with self.session.begin():
            mailing_dal = MailingDAL(self.session)
            mailings = mailing_dal.get_mailings()
            return None
