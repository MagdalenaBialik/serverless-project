from pydantic import BaseModel


class PetStatistics(BaseModel):
    pet_name: str
    count: int


class EventBridgeEvent(BaseModel):
    days: int
    email_title: str


# dict = {'days': '7', 'email_title': 'Pet of the days weekly statistics'}
# object = EventBridgeEvent.parse_obj(dict)
# print(object.days)
