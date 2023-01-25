from typing import Optional

from pydantic import BaseModel, validator


class PetStatistics(BaseModel):
    pet_name: str
    count: int


class EventBridgeEvent(BaseModel):
    days: Optional[int]
    email_title: str

    @validator("days", pre=True)
    def allow_none(cls, v):
        if v is None:
            return None
        else:
            return v


# dict = {'days': '7', 'email_title': 'Pet of the days weekly statistics'}
# object = EventBridgeEvent.parse_obj(dict)
# print(object.days)
