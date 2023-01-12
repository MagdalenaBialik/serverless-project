class Stream:
    def __init__(self, ses_service):
        self.ses_service = ses_service

    def get_pet_name_from_stream_event(self, event):
        image = event["Records"][0]["dynamodb"]["NewImage"]
        name = image["PK"]["S"]

        return name

    def ses_send(self, title: str, message):
        ses_response = self.ses_service.send_email(
            Source="magdalena.bialik@gmail.com",
            Destination={"ToAddresses": ["magdalena.bialik@gmail.com"]},
            Message={
                "Subject": {"Data": title},
                "Body": {"Text": {"Data": message}},
            },
        )
        return ses_response

    def send_stream(self, title, event):
        message = self.get_pet_name_from_stream_event(event)
        self.ses_send(title, message)

        return message
