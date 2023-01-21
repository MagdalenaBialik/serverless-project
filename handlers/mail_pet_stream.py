import json

from app.statistic_class import StatisticsSettings
from app.stream_class import Stream


def handler(event, context):
    print(event)
    stream = Stream.create()
    settings = StatisticsSettings()
    stream.send_mail_from_stream(settings.email_title, event)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
