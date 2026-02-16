"""Optional encryption/decryption helpers.

This project stores OAuth tokens in OAuthToken.access_token_enc / refresh_token_enc.
In development this may be plain text; in production you should encrypt at rest.

If ENCRYPTION_KEY is set (Fernet key), this module will attempt to decrypt tokens
that look like Fernet strings (typically starting with 'gAAAA').
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from django.conf import settings


def _get_fernet():
    key = getattr(settings, "ENCRYPTION_KEY", b"")
    if not key:
        return None
    try:
        from cryptography.fernet import Fernet

        return Fernet(key)
    except Exception:
        return None


def maybe_decrypt(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    # Common Fernet prefix. If token is plain, return as-is.
    if not isinstance(value, str):
        return value

    f = _get_fernet()
    if not f:
        return value

    if not value.startswith("gAAAA"):
        return value

    try:
        return f.decrypt(value.encode("utf-8")).decode("utf-8")
    except Exception:
        # If decryption fails, keep original to avoid hard-failing.
        return value
