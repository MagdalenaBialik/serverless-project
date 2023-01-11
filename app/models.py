from pydantic import BaseModel


class PetStatistics(BaseModel):
    pet_name: str
    count: int
