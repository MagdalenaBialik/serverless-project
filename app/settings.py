from typing import List, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    dynamodb_table_name: str
    pets: List[str] = ["Brutus", "Borys", "Majkus", "Milusia"]
    s3_bucket_name: str
    days: Optional[int]
    email_title: str


def get_settings():
    return Settings()
