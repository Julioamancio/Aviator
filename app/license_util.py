from __future__ import annotations

import base64
import hashlib
import hmac
from datetime import date, datetime, timedelta
from typing import Tuple


def _sign(secret: str, username: str, exp_ymd: str) -> str:
    msg = f"{username}|{exp_ymd}".encode("utf-8")
    mac = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(mac).decode("utf-8").rstrip("=")


def generate_license(secret: str, username: str, days: int) -> str:
    """Create a signed license token tied to username and expiry date.

    Format: username|YYYYMMDD|sig (sig is urlsafe base64 HMAC-SHA256)
    """
    exp = (date.today() + timedelta(days=int(days))).strftime("%Y%m%d")
    sig = _sign(secret, username, exp)
    return f"{username}|{exp}|{sig}"


def verify_license(secret: str, token: str, expected_username: str) -> Tuple[bool, str | date]:
    """Verify token signature and expiry.

    Returns (ok, exp_date or error_message)
    """
    try:
        parts = token.split("|")
        if len(parts) != 3:
            return False, "Invalid license format"
        username, exp, sig = parts
        if username.lower() != expected_username.lower():
            return False, "License does not match user"
        expected_sig = _sign(secret, username, exp)
        if not hmac.compare_digest(sig, expected_sig):
            return False, "Invalid signature"
        try:
            exp_date = datetime.strptime(exp, "%Y%m%d").date()
        except Exception:
            return False, "Invalid expiration date"
        if date.today() > exp_date:
            return False, "License expired"
        return True, exp_date
    except Exception:
        return False, "License verification failed"

