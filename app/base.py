from typing import List, Optional

from pydantic import BaseSettings


class SharedSettings(BaseSettings):
    dynamodb_table_name: str
    pets: List[str] = ["Brutus", "Borys", "Majkus", "Milusia"]


class StatisticsSettings(SharedSettings):
    s3_bucket_name: str
    days: Optional[int]
    email_title: str
