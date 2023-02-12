import random
from typing import List

from app.base import SharedSettings


class S3BucketDAO:
    def __init__(self, s3_client, settings: SharedSettings):
        self.s3_client = s3_client
        self.settings = settings

    def choose_rand_object_from_s3_bucket(self, prefix: str) -> List[str]:
        list_of_s3_objects = self.s3_client.list_objects_v2(
            Bucket=self.settings.s3_bucket_name, Prefix=prefix
        )["Contents"]
        return random.choice([obj["Key"] for obj in list_of_s3_objects])

    def generate_presigned_url(self, object_key):
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.settings.s3_bucket_name, "Key": object_key},
            ExpiresIn=3600,
        )
