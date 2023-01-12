import os

import boto3
import pytest

from app.stream_class import Stream


@pytest.fixture(autouse=True)
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"


@pytest.fixture()
def ses_client():
    return boto3.client(service_name="ses")


@pytest.fixture()
def stream(ses_client):
    return Stream(ses_service=ses_client)


@pytest.fixture()
def test_event():
    return {
        "Records": [
            {
                "eventID": "d4bddbb8d65f8ac6fbe85a64a940b1f1",
                "eventName": "INSERT",
                "eventVersion": "1.1",
                "eventSource": "aws:dynamodb",
                "awsRegion": "eu-west-1",
                "dynamodb": {
                    "ApproximateCreationDateTime": 1673322558.0,
                    "Keys": {"SK": {"N": "1673322558"}, "PK": {"S": "Milusia"}},
                    "NewImage": {"SK": {"N": "1673322558"}, "PK": {"S": "Milusia"}},
                    "SequenceNumber": "28902000000000058232616929",
                    "SizeBytes": 34,
                    "StreamViewType": "NEW_IMAGE",
                },
                "eventSourceARN": "arn:aws:dynamodb:eu-west-1:557918239263:table/pets-app-statistics-table/stream/2023-01-09T13:07:41.387",
            }
        ]
    }