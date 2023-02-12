from typing import Optional

from pydantic import BaseModel


class PetStatistics(BaseModel):
    pet_name: str
    count: int


class EventBridgeEvent(BaseModel):
    days: Optional[int]
    email_title: str
