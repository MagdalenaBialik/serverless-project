import random
from typing import List

from app.statistic_class import StatisticsSettings


class S3BucketDAO:
    def __init__(self, s3_client, settings: StatisticsSettings):
        self.s3_client = s3_client
        self.settings = settings

    def choose_rand_object_from_s3_bucket(self, prefix: str) -> List[str]:
        lista = self.s3_client.list_objects_v2(
            Bucket=self.settings.s3_bucket_name, Prefix=prefix
        )["Contents"]
        return random.choice([lista[i]["Key"] for i in range(0, len(lista))])
