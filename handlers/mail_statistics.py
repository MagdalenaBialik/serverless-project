import json

from app.base import StatisticsSettings
from app.statistic_class import Statistic


def handler(event, context):
    print(event)
    settings = StatisticsSettings()
    statistics_object = Statistic.create(settings)
    statistics_object.send_statistics(settings.email_title)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
