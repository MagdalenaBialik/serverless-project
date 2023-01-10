def get_pet_name_from_stream_event(event):
    image = event["Records"][0]["dynamodb"]["NewImage"]
    name = image["PK"]["S"]

    return name
