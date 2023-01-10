import json
from logging import getLogger

from app.statistics import StatisticsSettings, ses_send
from app.utils import get_pet_name_from_stream_event

logger = getLogger()
settings = StatisticsSettings()


def handler(event, context):
    name = get_pet_name_from_stream_event(event)
    ses_response = ses_send(settings.email_title, name)

    return {"statusCode": 200, "body": json.dumps(ses_response)}
