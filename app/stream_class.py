import boto3


class Stream:
    def __init__(self, ses_service):
        self.ses_service = ses_service

    @classmethod
    def create(cls):
        return cls(boto3.client(service_name="ses", region_name="eu-west-1"))

    def get_pet_name_from_stream_event(self, event: dict):
        return event["Records"][0]["dynamodb"]["NewImage"]["PK"]["S"]

    def ses_send(self, title: str, message: str):
        ses_response = self.ses_service.send_email(
            Source="magdalena.bialik@gmail.com",
            Destination={"ToAddresses": ["magdalena.bialik@gmail.com"]},
            Message={
                "Subject": {"Data": title},
                "Body": {"Text": {"Data": message}},
            },
        )
        return ses_response

    def send_mail_from_stream(self, title: str, event: dict):
        message = self.get_pet_name_from_stream_event(event)
        self.ses_send(title, message)

        return message
