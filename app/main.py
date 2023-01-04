import json
import random as rand
import time

import boto3

from app.settings import get_settings

settings = get_settings()

db_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    settings.DYNAMODB_TABLE_NAME
)


def add_to_table(pet_of_the_day):
    db_table.put_item(
        Item={"PK": pet_of_the_day, "SK": int(time.time())},
    )


def handler(event, context):
    pets = ["Brutus", "Borys", "Majkus", "Milusia"]
    pet_of_the_day = rand.choice(pets)

    add_to_table(pet_of_the_day)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
