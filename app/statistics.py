import json
import time
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Key

from app.settings import get_settings

settings = get_settings()

db_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    settings.dynamodb_table_name
)
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


def prepare_statistics_message(pet_statistics_dict):

    message = "Pet Statistics: \n"
    for pets_name, result in pet_statistics_dict.items():
        message += f"{pets_name}:{result}\n"

    message += get_object_from_s3(pet_statistics_dict)

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


def get_key_condition_expression(pet: str, days: Optional[int]):
    if days is None:
        return Key("PK").eq(pet)
    else:
        return Key("PK").eq(pet) & Key("SK").gt(
            int(time.time() - (days * 24 * 60 * 60))
        )


def statistics():
    pet_statistics_dict = {}
    for pet in settings.pets:
        response = db_table.query(
            Select="COUNT",
            KeyConditionExpression=get_key_condition_expression(
                pet=pet, days=settings.days
            ),
        )

        pet_statistics_dict[pet] = response["Count"]

    message_to_send = prepare_statistics_message(pet_statistics_dict)
    ses_send(settings.email_title, message_to_send)


def handler(event, context):
    statistics()
    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}


# print(get_key_condition_expression("Borys", 7))

statistics()
