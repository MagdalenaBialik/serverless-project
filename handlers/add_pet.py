import json

from app.base import SharedSettings
from app.dynamodb_dao import DynamoDBDao


def handler(event, context):
    settings = SharedSettings()
    dao = DynamoDBDao.create(settings)
    dao.add_random_pet()

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
