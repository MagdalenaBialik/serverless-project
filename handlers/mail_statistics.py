import json

from app.base import SharedSettings
from app.statistic_class import Statistic


def handler(event, context):
    print(event)
    print(event["days"])
    print(event["email_title"])
    settings = SharedSettings()
    statistics_object = Statistic.create(settings)
    statistics_object.send_statistics(
        days=int(event["days"]), title=event["email_title"]
    )

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
