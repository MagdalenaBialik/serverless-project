import json

from app.base import SharedSettings
from app.dynamodb_dao import DynamoDBDao


def handler(event, context):
    settings = SharedSettings()
    dao = DynamoDBDao(settings=settings)

    dao.add_pet()

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
