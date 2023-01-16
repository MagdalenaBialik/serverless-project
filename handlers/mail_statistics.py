import json

import boto3

from app.base import StatisticsSettings
from app.statistic_class import Statistic

settings = StatisticsSettings()

dynamodb_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
    settings.dynamodb_table_name
)

s3 = boto3.client(service_name="s3", region_name="eu-west-1")
ses_client = boto3.client(service_name="ses", region_name="eu-west-1")

statistics_object = Statistic(
    dynamodb_table=dynamodb_table,
    s3_client=s3,
    ses_service=ses_client,
    settings=settings,
)


def handler(event, context):
    statistics_object.send_statistics(settings.email_title)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
