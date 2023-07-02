import datetime
from uuid import UUID
from logging import getLogger
import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from schemas.mailings import (
    ShowMailing,
    MailingCreate,
    MailingsStats,
    MailingStats,
    MailingDeleteResponse
)
from services import MailingService, MessageService

logger = getLogger(__name__)

mailing_router = APIRouter()


@mailing_router.post("/")
async def create_mailing(
        body: MailingCreate,
        mailing_service: MailingService = Depends(),
) -> ShowMailing:
    try:
        # return await MessageService().send_message(999, datetime.datetime.now())
        mailing = await mailing_service.create(
            body
        )
        return mailing
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )


@mailing_router.get("/stats")
async def get_mailings_stats(
        mailing_service: MailingService = Depends()
) -> MailingsStats:
    return await mailing_service.get_mailings_stats()


@mailing_router.get("/detailed_stats")
async def get_mailing_stat(
        mailing_id: UUID,
        mailing_service: MailingService = Depends()
) -> MailingStats:

    mailing_stats = await mailing_service.get_mailing_stats(mailing_id)
    if not mailing_stats:
        raise HTTPException(
            status_code=404,
            detail=f"Mailing with {mailing_id} id is not found"
        )
    return mailing_stats


@mailing_router.delete("/")
async def delete_mailing(
        mailing_id: UUID,
        mailing_service: MailingService = Depends()
) -> MailingDeleteResponse:
    deleted_mailing_id = await mailing_service.delete(mailing_id)
    if not deleted_mailing_id:
        raise HTTPException(
            status_code=404,
            detail=f"Mailing with {mailing_id} is not found"
        )
    return MailingDeleteResponse(
        deleted_mailing_id=deleted_mailing_id
    )
