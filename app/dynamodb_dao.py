import random as rand
import time
from typing import List, Optional

import boto3
from boto3.dynamodb.conditions import Key

from app.base import SharedSettings
from app.models import PetStatistics


class DynamoDBDao:
    def __init__(self, dynamodb_table, settings: SharedSettings):
        self.settings = settings
        self.dynamodb_table = dynamodb_table

    @classmethod
    def create(cls, settings):
        return cls(
            boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
                settings.dynamodb_table_name
            ),
            settings,
        )

    def add_pet(self, pet_name: str):
        self.dynamodb_table.put_item(
            Item={"PK": pet_name, "SK": int(time.time())},
        )

    def add_random_pet(self):
        pet_name = rand.choice(self.settings.pets)
        self.add_pet(pet_name=pet_name)

    @staticmethod
    def get_key_condition_expression(pet: str, days: Optional[int]):
        if days is None:
            return Key("PK").eq(pet)
        return Key("PK").eq(pet) & Key("SK").gt(
            int(time.time() - (days * 24 * 60 * 60))
        )

    def get_all_pet_events_by_name(
        self, pet_name: str, days: Optional[int]
    ) -> PetStatistics:
        response = self.dynamodb_table.query(
            Select="COUNT",
            KeyConditionExpression=self.get_key_condition_expression(
                pet=pet_name, days=days
            ),
        )
        return PetStatistics(pet_name=pet_name, count=response["Count"])

    def get_all_pet_event(self, days: Optional[int]) -> List[PetStatistics]:
        pet_events = [
            self.get_all_pet_events_by_name(pet, days) for pet in self.settings.pets
        ]
        return pet_events
