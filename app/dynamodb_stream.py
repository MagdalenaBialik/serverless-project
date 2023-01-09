import json

from app.statistics import ses_send


def handler(event, context):
    image = event["Records"][0]["dynamodb"]["NewImage"]
    imie = image["PK"]["S"]
    ses_response = ses_send("Pet of the day", imie)

    return {"statusCode": 200, "body": json.dumps(ses_response)}
