import json

import boto3

from app.base import SharedSettings
from app.dynamodb_dao import DynamoDBDao


def handler(event, context):
    settings = SharedSettings()

    db_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
        settings.dynamodb_table_name
    )

    dao = DynamoDBDao(dynamodb_table=db_table, settings=settings)

    dao.add_random_pet()

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
