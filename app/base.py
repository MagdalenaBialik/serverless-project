from typing import List

from pydantic import BaseSettings


class SharedSettings(BaseSettings):
    dynamodb_table_name: str
    pets: List[str] = ["Brutus", "Borys", "Majkus", "Milusia"]
    s3_bucket_name: str


# class StatisticsSettings(SharedSettings):
#
#     days: Optional[int]
#     email_title: str
