from typing import Optional
import re
from uuid import UUID

from fastapi import HTTPException

from pydantic import BaseModel
from pydantic import validator


PHONE_NUMBER_MATCH_PATTERN = re.compile(r"\b7[\d]{10}\b")


class TunedModel(BaseModel):
    """for pydantic converting to json any objects even not dict"""

    class Config:
        orm_mode = True


class ShowRecipient(TunedModel):
    recipient_id: UUID
    phone_number: str
    mobile_code: str
    time_zone: str
    tag: Optional[str]



class RecipientCreate(BaseModel):
    phone_number: str
    time_zone: str
    tag: Optional[str]

    @validator('phone_number')
    def validate_phone_number(cls, value):
        if not PHONE_NUMBER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail='Phone number should match 7XXXXXXXXXX template'
            )
        return value


class RecipientDeleteResponse(BaseModel):
    deleted_recipient_id: UUID


class RecipientUpdateResponse(BaseModel):
    updated_recipient_id: UUID


class RecipientUpdate(BaseModel):
    phone_number: Optional[str]
    time_zone: Optional[str]
    tag: Optional[str]

    @validator('phone_number')
    def validate_phone_number(cls, value):
        if not PHONE_NUMBER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail='Phone number should match 7XXXXXXXXXX template'
            )
        return value
