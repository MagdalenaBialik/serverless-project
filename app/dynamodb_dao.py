import random as rand

from app.base import SharedSettings


class DynamoDBDao:
    def __init__(self, settings: SharedSettings):
        self.settings = settings

    def add_pet(self, pet_name):
        pass

    def add_random_pet(self):
        pet_name = rand.choice(self.settings.pets)
        self.add_pet(pet_name=pet_name)
