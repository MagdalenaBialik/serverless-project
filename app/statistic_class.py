import operator
from typing import List

from app.base import StatisticsSettings
from app.dynamodb_dao import DynamoDBDao
from app.models import PetStatistics
from app.s3_dao import S3BucketDAO


class Statistic:
    def __init__(
        self,
        dynamodb_table,
        s3_client,
        ses_service,
        settings: StatisticsSettings,
    ):
        self.s3_client = s3_client
        self.ses_service = ses_service
        self.settings = settings

        self.dynamodb_dao = DynamoDBDao(
            dynamodb_table=dynamodb_table, settings=settings
        )

    def get_presigned_url(self, pet_statistics: List[PetStatistics]):
        max_pet_statistics = max(pet_statistics, key=operator.attrgetter("count"))
        s3_bucket_dao = S3BucketDAO(s3_client=self.s3_client, settings=self.settings)
        object_key = s3_bucket_dao.choose_rand_object_from_s3_bucket(max_pet_statistics)

        url = self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.settings.s3_bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )
        return url

    def prepare_statistics_message(self, pet_statistics: List[PetStatistics]):
        message = "Pet Statistics: \n"
        for item in pet_statistics:
            message += f"{item.pet_name}:{item.count}\n"

        message += self.get_presigned_url(pet_statistics)

        return message

    def send_statistics(self, title: str):
        pet_events = self.dynamodb_dao.get_all_pet_event(days=self.settings.days)
        message = self.prepare_statistics_message(pet_events)

        self.ses_send(title, message)
        return message

    def ses_send(self, title: str, message):
        ses_response = self.ses_service.send_email(
            Source="magdalena.bialik@gmail.com",
            Destination={"ToAddresses": ["magdalena.bialik@gmail.com"]},
            Message={
                "Subject": {"Data": title},
                "Body": {"Text": {"Data": message}},
            },
        )
        return ses_response
