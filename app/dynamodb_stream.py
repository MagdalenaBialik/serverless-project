import json

from app.statistics import StatisticsSettings, ses_send

settings = StatisticsSettings()


def handler(event, context):
    image = event["Records"][0]["dynamodb"]["NewImage"]
    imie = image["PK"]["S"]
    ses_response = ses_send(settings.email_title, imie)

    return {"statusCode": 200, "body": json.dumps(ses_response)}
