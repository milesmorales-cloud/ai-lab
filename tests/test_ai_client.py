from ai_client import send_message


def test_send_message():
    assert callable(send_message)