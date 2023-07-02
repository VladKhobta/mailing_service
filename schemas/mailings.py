from typing import Optional
import re
from uuid import UUID
from datetime import datetime

from fastapi import HTTPException

from pydantic import BaseModel
from pydantic import validator, root_validator


class TunedModel(BaseModel):

    class Config:
        orm_mode = True


class ShowMailing(TunedModel):
    mailing_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    content: str
    tag_filter: Optional[str] = None
    mobile_code_filter: Optional[str] = None


class MailingCreate(BaseModel):
    start_datetime: datetime
    end_datetime: datetime
    content: str
    tag_filter: Optional[str] = None
    mobile_code_filter: Optional[str] = None

    @root_validator
    def validate_filters(cls, values):
        if not (values['tag_filter'] or values['mobile_code_filter']):
            raise HTTPException(
                status_code=422,
                detail="At least one of tag_filter or mobile_code_filter must have a value"
            )
        return values

    @root_validator
    def validate_start_datetime(cls, values):
        if values.get('start_datetime') > values.get('end_datetime'):
            raise HTTPException(
                status_code=422,
                detail=f'Start datetime cannot be greater than end datetime'
            )
        return values


class MailingsStats(TunedModel):
    mailings_count: int
    messages_count: int
    pending_messages: int
    failed_messages: int
    sent_messages: int


class MailingStats(TunedModel):
    mailing_id: UUID
    content: str
    recipients_count: int
    messages_count: int
    pending_messages: int
    failed_messages: int
    sent_messages: int


class MailingDeleteResponse(TunedModel):
    deleted_mailing_id: UUID
