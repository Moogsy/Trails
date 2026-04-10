from exponent_server_sdk import PushClient, PushMessage
from config import settings

_client = PushClient()


def send_push(expo_token: str, title: str, body: str, data: dict | None = None) -> None:
    _client.publish(
        PushMessage(
            to=expo_token,
            title=title,
            body=body,
            data=data or {},
        )
    )
