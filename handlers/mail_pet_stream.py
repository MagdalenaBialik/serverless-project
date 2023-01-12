import json

import boto3

from app.statistic_class import StatisticsSettings
from app.stream_class import Stream

s3 = boto3.client(service_name="s3", region_name="eu-west-1")
stream = Stream(s3)


def handler(event, context):
    settings = StatisticsSettings()
    stream.send_stream(settings.email_title, event)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
