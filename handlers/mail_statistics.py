import json

from app.base import SharedSettings
from app.models import EventBridgeEvent
from app.statistic_class import Statistic


def handler(event, context):
    print(event)
    settings = SharedSettings()
    statistics_object = Statistic.create(settings)
    event_object = EventBridgeEvent.parse_obj(event)
    statistics_object.send_statistics(
        days=event_object.days, title=event_object.email_title
    )

    return {"statusCode": 200, "body": json.dumps("Hello from lambda")}
