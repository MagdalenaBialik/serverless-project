import operator
from typing import List, Optional

from app.base import SharedSettings
from app.dynamodb_dao import DynamoDBDao
from app.models import PetStatistics


class StatisticsSettings(SharedSettings):
    s3_bucket_name: str
    days: Optional[int]
    email_title: str


class Statistic:
    def __init__(
        self, dynamodb_table, s3_bucket, ses_service, settings: StatisticsSettings
    ):
        self.dynamodb_table = dynamodb_table
        self.s3_bucket = s3_bucket
        self.ses_service = ses_service
        self.settings = settings

    def get_object_from_s3(self, pet_statistics: List[PetStatistics]):
        max_pet_statistics = max(pet_statistics, key=operator.attrgetter("count"))

        object_key = f"{max_pet_statistics.pet_name}.jpg"

        url = self.s3_bucket.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.settings.s3_bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )
        return url

    def prepare_statistics_message(self, pet_statistics: List[PetStatistics]):
        message = "Pet Statistics: \n"
        for item in pet_statistics:
            message += f"{item.pet_name}:{item.count}\n"

        message += self.get_object_from_s3(pet_statistics)

        return message

    def ses_send(self, title: str):
        dao = DynamoDBDao(dynamodb_table=self.dynamodb_table, settings=self.settings)
        pet_events = dao.get_all_pet_event(days=self.settings.days)
        message = self.prepare_statistics_message(pet_events)

        ses_response = self.ses_service.send_email(
            Source="magdalena.bialik@gmail.com",
            Destination={"ToAddresses": ["magdalena.bialik@gmail.com"]},
            Message={
                "Subject": {"Data": title},
                "Body": {"Text": {"Data": message}},
            },
        )
        return ses_response
