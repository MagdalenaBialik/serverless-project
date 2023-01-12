import json

import boto3

from app.statistic_class import StatisticsSettings
from app.stream_class import Stream

ses_client = boto3.client(service_name="ses", region_name="eu-west-1")
stream = Stream(ses_client)


def handler(event, context):
    settings = StatisticsSettings()
    stream.send_mail_from_stream(settings.email_title, event)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
