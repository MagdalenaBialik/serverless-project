from pydantic import BaseSettings


class Settings(BaseSettings):
    DYNAMODB_TABLE_NAME: str


def get_settings():
    return Settings()
