import datetime
from uuid import UUID
from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import MessageDAL, MailingDAL, RecipientDAL
from db.session import get_db
from db.models import Recipient, Message, Mailing
from db.models.messages import MessageStatus
from schemas.mailings import (
    ShowMailing,
    MailingCreate,
    MailingsStats,
    MailingStats
)
from db.session import async_session
from services.scheduling import scheduler
from services import MessageService


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

            recipient_dal = RecipientDAL(self.session)
            recipients = await recipient_dal.get_by_filters(
                mailing.tag_filter,
                mailing.mobile_code_filter
            )

        if recipients:
            await self.schedule_mailing(
                mailing,
                recipients
            )

        return ShowMailing(
            mailing_id=mailing.mailing_id,
            start_datetime=mailing.start_datetime,
            end_datetime=mailing.end_datetime,
            content=mailing.content,
            tag_filter=mailing.tag_filter,
            mobile_code_filter=mailing.mobile_code_filter
        )

    async def delete(
            self,
            mailing_id: UUID,
    ) -> Union[UUID, None]:
        async with self.session.begin():
            messages_dal = MessageDAL(self.session)

            await messages_dal.delete_related_to_mailing(mailing_id)

            mailing_dal = MailingDAL(self.session)
            deleted_mailing_id = await mailing_dal.delete(
                mailing_id=mailing_id
            )

            return deleted_mailing_id



    async def get_mailings_stats(self) -> MailingsStats:
        async with self.session.begin():
            mailing_dal = MailingDAL(self.session)
            messages_dal = MessageDAL(self.session)

            mailings_count = await mailing_dal.get_mailings_count()
            sent_count = await messages_dal.get_status_count(MessageStatus.SENT)
            pending_count = await messages_dal.get_status_count(MessageStatus.PENDING)
            failed_count = await messages_dal.get_status_count(MessageStatus.FAILED)
            print(mailings_count)

            return MailingsStats(
                mailings_count=mailings_count,
                messages_count=pending_count+failed_count+sent_count,
                pending_messages=pending_count,
                failed_messages=failed_count,
                sent_messages=sent_count
            )

    async def get_mailing_stats(
            self,
            mailing_id: UUID
    ) -> Union[MailingStats, None]:
        async with self.session.begin():
            mailing_dal = MailingDAL(self.session)
            mailing = await mailing_dal.get_mailing_by_id(
                mailing_id=mailing_id
            )

        if not mailing:
            return None

        return MailingStats(
            mailing_id=mailing_id,
            content=mailing.content,
            tag_filter=mailing.tag_filter,
            mobile_code_filter=mailing.mobile_code_filter,
            recipients_count=0,
            messages_count=0,
            pending_messages=0,
            failed_messages=0,
            sent_messages=0
        )

    async def schedule_mailing(
            self,
            mailing: Mailing,
            recipients: [Recipient]
    ):
        for recipient in recipients:
            await self.schedule_message(mailing, recipient)

    async def schedule_message(
            self,
            mailing: Message,
            recipient: Recipient
    ):
        message_dal = MessageDAL(self.session)
        now = datetime.datetime.now(datetime.timezone.utc)

        if mailing.end_datetime < now:
            print('fail')
            await message_dal.create(
                recipient_id=recipient.recipient_id,
                mailing_id=mailing.mailing_id,
                status=MessageStatus.FAILED
            )
        else:
            message = await message_dal.create(
                recipient_id=recipient.recipient_id,
                mailing_id=mailing.mailing_id,
                status=MessageStatus.PENDING
            )
            message_service = MessageService(async_session())
            if mailing.start_datetime <= now:
                scheduler.add_job(
                    message_service.send_message,
                    args=[
                        message.message_id,
                        recipient.phone_number,
                        mailing.content,
                        mailing.end_datetime
                    ],
                    id=str(message.message_id)
                )
            else:
                scheduler.add_job(
                    message_service.send_message,
                    args=[
                        message.message_id,
                        recipient.phone_number,
                        mailing.content,
                        mailing.end_datetime
                    ],
                    id=str(message.message_id),
                    run_date=mailing.start_datetime
                )
