import json
from typing import List, Optional

import boto3

from app.base import SharedSettings
from app.dynamodb_dao import DynamoDBDao
from app.models import PetStatistics


class StatisticsSettings(SharedSettings):
    s3_bucket_name: str
    days: Optional[int]
    email_title: str


settings = StatisticsSettings()

db_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    settings.dynamodb_table_name
)

dao = DynamoDBDao(db_table, settings)

s3 = boto3.client(service_name="s3", region_name="eu-west-1")
ses_client = boto3.client(service_name="ses", region_name="eu-west-1")


def get_object_from_s3(pet_statistics_dict):
    max_pet_statistics_dict = max(pet_statistics_dict, key=pet_statistics_dict.get)

    object_key = f"{max_pet_statistics_dict}.jpg"

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket_name, "Key": object_key},
        ExpiresIn=3600,
    )

    return url


def prepare_statistics_message(pet_statistics: List[PetStatistics]):
    message = "Pet Statistics: \n"
    for index in range(0, len(pet_statistics)):
        item = pet_statistics[index]
        message += f"{item.pet_name}:{item.count}\n"

    # message += get_object_from_s3(pet_statistics_dict)

    return message


def ses_send(title, message):
    ses_response = ses_client.send_email(
        Source="magdalena.bialik@gmail.com",
        Destination={"ToAddresses": ["magdalena.bialik@gmail.com"]},
        Message={
            "Subject": {"Data": title},
            "Body": {"Text": {"Data": message}},
        },
    )
    return ses_response


def statistics():
    pet_events = dao.get_all_pet_event(days=None)
    message_to_send = prepare_statistics_message(pet_events)
    # ses_send(settings.email_title, message_to_send)
    return message_to_send


def handler(event, context):
    statistics()
    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}


print(statistics())
