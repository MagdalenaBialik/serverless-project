from moto import mock_ses


def test_get_pet_name_from_stream_event(stream, test_event):
    response = stream.get_pet_name_from_stream_event(test_event)
    assert response == "Milusia"


@mock_ses
def test_send_mail_from_stream(ses_client, stream, test_event):
    ses_client.verify_email_identity(EmailAddress="magdalena.bialik@gmail.com")

    response = stream.send_mail_from_stream(title="Title", event=test_event)
    assert response == "Milusia"
