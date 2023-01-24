import json

from app.base import SharedSettings
from app.statistic_class import Statistic


def handler(event, context):
    settings = SharedSettings()
    statistics_object = Statistic.create(settings)
    statistics_object.send_statistics(days=event["days"], title=event["email_title"])

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
