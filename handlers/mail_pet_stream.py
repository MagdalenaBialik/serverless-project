import json

from app.base import StreamSettings
from app.stream_class import Stream


def handler(event, context):
    stream = Stream.create()
    settings = StreamSettings()
    stream.send_mail_from_stream(settings.email_title, event)

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
