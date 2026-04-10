import hashlib
import hmac
from config import settings


def hash_phone(phone: str) -> str:
    return hmac.new(
        settings.phone_hash_secret.encode(),
        phone.encode(),
        hashlib.sha256,
    ).hexdigest()


def hash_device(device_id: str) -> str:
    return hmac.new(
        settings.device_hash_secret.encode(),
        device_id.encode(),
        hashlib.sha256,
    ).hexdigest()
