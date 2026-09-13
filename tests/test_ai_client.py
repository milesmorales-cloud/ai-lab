from unittest.mock import Mock, patch

import requests

from ai_client import send_message


@patch("ai_client.requests.post")
def test_send_message(mock_post):
    fake_response = Mock()

    fake_response.status_code = 200
    fake_response.json.return_value = {
        "model": "fake-model",
        "choices": [
            {
                "message": {
                    "content": "Hello mate!"
                }
            }
        ]
    }

    mock_post.return_value = fake_response

    result = send_message([
        {
            "role": "user",
            "content": "Say hello"
        }
    ])

    assert result["model"] == "fake-model"
    assert result["message"] == "Hello mate!"


@patch("ai_client.requests.post")
def test_send_message_handles_api_error(mock_post):
    fake_response = Mock()

    fake_response.status_code = 500
    fake_response.json.return_value = {
        "error": {
            "message": "Server error"
        }
    }

    mock_post.return_value = fake_response

    try:
        send_message([
            {
                "role": "user",
                "content": "Hello"
            }
        ])
        assert False, "Expected RuntimeError"
    except RuntimeError as error:
        assert "OpenRouter error" in str(error)

@patch("ai_client.requests.post")
def test_send_message_handles_network_error(mock_post):
    mock_post.side_effect = requests.exceptions.RequestException(
        "Connection failed"
    )

    try:
        send_message([
            {
                "role": "user",
                "content": "Hello"
            }
        ])
        assert False, "Expected RuntimeError"
    except RuntimeError as error:
        assert str(error) == "Unable to connect to OpenRouter."        