from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.exc import IntegrityError

from schemas.recipients import (
    ShowRecipient,
    RecipientCreate, RecipientUpdate,
    RecipientDeleteResponse, RecipientUpdateResponse
)

from services.recipients import RecipientService


logger = getLogger(__name__)

recipient_router = APIRouter()


@recipient_router.post("/")
async def create_recipient(
        body: RecipientCreate,
        recipient_service: RecipientService = Depends()
) -> ShowRecipient:
    try:
        return await recipient_service.create(
            phone_number=body.phone_number,
            time_zone=body.time_zone,
            tag=body.tag
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f'Database error: {err}'
        )


@recipient_router.delete('/')
async def delete_recipient(
        recipient_id: UUID,
        recipient_service: RecipientService = Depends()
) -> RecipientDeleteResponse:
    deleted_recipient_id = await recipient_service.delete(recipient_id)
    if deleted_recipient_id is None:
        raise HTTPException(
            status_code=404,
            detail=f"Recipient with {recipient_id} id is not found"
        )
    return RecipientDeleteResponse(
        deleted_recipient_id=deleted_recipient_id
    )


@recipient_router.patch("/")
async def update_recipient_by_id(
        recipient_id: UUID,
        body: RecipientUpdate,
        recipient_service: RecipientService = Depends()
) -> RecipientUpdateResponse:
    updated_recipient_data = body.dict(exclude_none=True)
    if updated_recipient_data == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one of recipient parameters must be provided"
        )
    recipient = await recipient_service.get_by_id(recipient_id)
    if recipient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Recipient with {recipient_id} id is not found"
        )
    try:
        updated_recipient_id = await recipient_service.update(
            recipient_id=recipient_id,
            recipient_updated_data=updated_recipient_data
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(
            status_code=503,
            detail=f"Database error: {err}"
        )
    return RecipientUpdateResponse(
        updated_recipient_id=updated_recipient_id
    )


@recipient_router.get("/")
async def get_recipient_by_id(
        recipient_id: UUID,
        recipient_service: RecipientService = Depends()
) -> ShowRecipient:
    recipient = await recipient_service.get_by_id(recipient_id)
    if recipient is None:
        raise HTTPException(
            status_code=404,
            detail=f"Recipient with {recipient_id} id is not found"
        )
    return recipient
