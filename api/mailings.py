import datetime
from uuid import UUID
from logging import getLogger
import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from schemas.mailings import (
    ShowMailing, MailingCreate,
    MailingsStats, MailingStats,
    MailingDeleteResponse, MailingUpdateResponse,
    MailingUpdate
)
from services import MailingService

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
async def get_detailed_mailing_stat(
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


@mailing_router.patch("/")
async def update_mailing(
        mailing_id: UUID,
        body: MailingUpdate,
        mailing_service: MailingService = Depends()
) -> MailingUpdateResponse:
    updated_mailing_data = body.dict(exclude_none=True)
    if updated_mailing_data == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one of mailing parameters must be provided"
        )
    mailing = await mailing_service.get_by_id(mailing_id)
    if mailing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Mailing with {mailing_id} id is not found"
        )
    now = datetime.datetime.now(datetime.timezone.utc)
    if mailing.start_datetime < now:
        raise HTTPException(
            status_code=403,
            detail=f"Started mailing cannot be modified"
        )
    try:
        updated_mailing_id = await mailing_service.update(
            mailing_id=mailing_id,
            updated_mailing_data=updated_mailing_data
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )
    return MailingUpdateResponse(
        updated_mailing_id=updated_mailing_id
    )