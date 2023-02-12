from typing import Optional

from pydantic import BaseModel


class PetStatistics(BaseModel):
    pet_name: str
    count: int


class EventBridgeEvent(BaseModel):
    days: Optional[int]
    email_title: str
    #
    # @validator("days", pre=True)
    # def allow_none(cls, v):
    #     # TODO: check if this is necessary
    #     if v is None:
    #         return None
    #     else:
    #         return v
