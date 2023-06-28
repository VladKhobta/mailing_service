from uuid import UUID
from logging import getLogger
import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from schemas.mailings import (
    ShowMailing,
    MailingCreate
)
from services.mailings import MailingService


logger = getLogger(__name__)

mailing_router = APIRouter()


@mailing_router.post("/")
async def create_mailing(
    body: MailingCreate,
    mailing_service: MailingService = Depends()
) -> ShowMailing:
    try:
        return await mailing_service.create(body)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )


@mailing_router.get("/")
async def get_mailings(
    mailing_service: MailingService = Depends()
):
    return await mailing_service.get_mailings()
