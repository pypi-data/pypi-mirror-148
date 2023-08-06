import hashlib
import hmac

from typing import Optional


def generate_mac(
    shared_secret: str,
    nonce: str,
    user: str,
    password: str,
    admin: bool = False,
    user_type: Optional[str] = None,
) -> str:

    shared_secret_key = shared_secret.encode("utf-8")
    mac = hmac.new(
        key=shared_secret_key,
        digestmod=hashlib.sha1,
    )

    mac.update(nonce.encode("utf8"))
    mac.update(b"\x00")
    mac.update(user.encode("utf8"))
    mac.update(b"\x00")
    mac.update(password.encode("utf8"))
    mac.update(b"\x00")
    mac.update(b"admin" if admin else b"notadmin")
    if user_type:
        mac.update(b"\x00")
        mac.update(user_type.encode("utf8"))

    return mac.hexdigest()
