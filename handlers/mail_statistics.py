import json

import boto3

from app.statistic_class import Statistic, StatisticsSettings

settings = StatisticsSettings()

s3 = boto3.client(service_name="s3", region_name="eu-west-1")
ses_client = boto3.client(service_name="ses", region_name="eu-west-1")

statistics_object = Statistic(
    s3_client=s3,
    ses_service=ses_client,
    settings=settings,
)


def handler(event, context):
    statistics_object.ses_send(settings.email_title)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
