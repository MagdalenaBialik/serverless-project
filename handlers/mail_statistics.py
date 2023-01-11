import json

import boto3

from app.dynamodb_dao import DynamoDBDao
from app.statistic_class import Statistic, StatisticsSettings


def handler(event, context):
    settings = StatisticsSettings()

    db_table = boto3.resource(service_name="dynamodb", region_name="eu-west-1").Table(
        settings.dynamodb_table_name
    )
    dao = DynamoDBDao(db_table, settings)

    s3 = boto3.client(service_name="s3", region_name="eu-west-1")
    ses_client = boto3.client(service_name="ses", region_name="eu-west-1")

    statistics_object = Statistic(db_table, s3, ses_client, settings)

    def statistics():
        pet_events = dao.get_all_pet_event(days=settings.days)
        message_to_send = statistics_object.prepare_statistics_message(pet_events)
        statistics_object.ses_send(settings.email_title, message_to_send)
        return message_to_send

    statistics()
    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
