import json
import time

import boto3
from boto3.dynamodb.conditions import Key

from app.settings import get_settings

settings = get_settings()

db_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    settings.dynamodb_table_name
)
s3 = boto3.client(service_name="s3", region_name="eu-west-1")


def get_object_from_s3(pet_statistics_dict):
    max_pet_statistics_dict = max(pet_statistics_dict, key=pet_statistics_dict.get)

    object_key = f"{max_pet_statistics_dict}.jpg"

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket_name, "Key": object_key},
        ExpiresIn=3600,
    )

    return url


def statistics():
    pet_statistics_dict = {}
    for pet in settings.pets:
        response = db_table.query(
            Select="COUNT",
            KeyConditionExpression=(
                Key("PK").eq(pet) & Key("SK").gt(int(time.time() - (7 * 24 * 60 * 60)))
            ),
        )
        pet_statistics_dict[pet] = response["Count"]
        response = get_object_from_s3(pet_statistics_dict)

    return response


def handler(event, context):
    statistics()
    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}


#
# def lambda_prepare_message(pet_statistics_dict):
#     max_pet_statistics_dict = max(pet_statistics_dict, key=pet_statistics_dict.get)
#
#     message = "Pet Statistics: \n"
#     for nazwa_zwierzatka, wynik in pet_statistics_dict.items():
#         message += f"{nazwa_zwierzatka}:{wynik}\n"
#
#     message += get_object_from_s3(pet_statistics_dict)
#     return message
#
#
# def lambda_sent_pet(message):
#     ses_response = ses_client.send_email(
#         Source='alek.fidelus@gmail.com',
#         Destination={
#             'ToAddresses': ['magdalena.bialik@gmail.com', 'alek.fidelus@gmail.com']
#         },
#         Message={
#             'Subject': {
#                 'Data': 'Statystyki zwierzatek dnia'
#             },
#
#             'Body': {
#                 'Text': {
#                     'Data': message
#                 }
#             }
#         }
#     )
#     return ses_response
