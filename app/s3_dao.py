import random
from typing import List

from app.base import StatisticsSettings
from app.models import PetStatistics


class S3BucketDAO:
    def __init__(self, s3_client, settings: StatisticsSettings):
        self.s3_client = s3_client
        self.settings = settings

    def choose_rand_object_from_s3_bucket(self, prefix: PetStatistics) -> List[str]:
        list_of_s3_objects = self.s3_client.list_objects_v2(
            Bucket=self.settings.s3_bucket_name, Prefix=prefix.pet_name
        )["Contents"]
        return random.choice([i["Key"] for i in list_of_s3_objects])
