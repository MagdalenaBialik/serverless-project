from typing import List

from pydantic import BaseSettings


class SharedSettings(BaseSettings):
    dynamodb_table_name: str
    pets: List[str] = ["Brutus", "Borys", "Majkus", "Milusia"]
