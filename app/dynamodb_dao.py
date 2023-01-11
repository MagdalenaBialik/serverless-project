import random as rand
import time

from app.base import SharedSettings


class DynamoDBDao:
    def __init__(self, dynamodb_table, settings: SharedSettings):
        self.settings = settings
        self.dynamodb_table = dynamodb_table

    def add_pet(self, pet_name: str):
        self.dynamodb_table.put_item(
            Item={"PK": pet_name, "SK": int(time.time())},
        )

    def add_random_pet(self):
        pet_name = rand.choice(self.settings.pets)
        self.add_pet(pet_name=pet_name)
