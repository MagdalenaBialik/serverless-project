import operator
import timeit
from typing import List

import boto3

from app.base import StatisticsSettings
from app.dynamodb_dao import DynamoDBDao
from app.models import PetStatistics
from app.s3_dao import S3BucketDAO


def timer(func):
    def wrapper(*args, **kwargs):
        t0 = timeit.default_timer()
        response = func(*args, **kwargs)
        t1 = timeit.default_timer()
        elapsed_time = t1 - t0
        print(f"elapsed time: {elapsed_time} for {func}")
        return response

    return wrapper


class Statistic:
    def __init__(
        self,
        dynamodb_table,
        s3_client,
        ses_service,
        settings: StatisticsSettings,
    ):
        self.ses_service = ses_service
        self.settings = settings

        self.dynamodb_dao = DynamoDBDao(
            dynamodb_table=dynamodb_table, settings=settings
        )
        self.s3_bucket_dao = S3BucketDAO(s3_client=s3_client, settings=self.settings)

    @classmethod
    def create(cls, settings):
        return cls(
            dynamodb_table=boto3.resource(
                service_name="dynamodb", region_name="eu-west-1"
            ).Table(settings.dynamodb_table_name),
            s3_client=boto3.client(service_name="s3", region_name="eu-west-1"),
            ses_service=boto3.client(service_name="ses", region_name="eu-west-1"),
            settings=settings,
        )

    def get_presigned_url(self, pet_statistics: List[PetStatistics]):
        max_pet_statistics = max(pet_statistics, key=operator.attrgetter("count"))
        object_key = self.s3_bucket_dao.choose_rand_object_from_s3_bucket(
            max_pet_statistics.pet_name
        )
        url = self.s3_bucket_dao.generate_presigned_url(object_key)
        return url

    @timer
    def prepare_statistics_message(self, pet_statistics: List[PetStatistics]):
        message = "Pet Statistics: \n"
        for item in pet_statistics:
            message += f"{item.pet_name}:{item.count}\n"

        message += self.get_presigned_url(pet_statistics)

        return message

    @timer
    def send_statistics(self, title: str):
        pet_events = self.dynamodb_dao.get_all_pet_event(days=self.settings.days)
        message = self.prepare_statistics_message(pet_events)

        self.ses_send(title, message)
        return message

    @timer
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
