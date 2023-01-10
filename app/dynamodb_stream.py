import json
from logging import getLogger

from app.statistics import StatisticsSettings, ses_send

logger = getLogger()
settings = StatisticsSettings()
#
# def get_pet_name_from_stream_event(event):
#     image = event["Records"][0]["dynamodb"]["NewImage"]
#     name = image["PK"]["S"]


def handler(event, context):
    image = event["Records"][0]["dynamodb"]["NewImage"]
    name = image["PK"]["S"]
    print(event)
    logger.info(event)
    ses_response = ses_send(settings.email_title, name)

    return {"statusCode": 200, "body": json.dumps(ses_response)}
